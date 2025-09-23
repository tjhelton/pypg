import asyncio
import csv
import os
import time
from datetime import datetime
from typing import Dict, List, Set

import aiohttp

TOKEN = os.environ.get('SAFETYCULTURE_TOKEN', '')
BASE_URL = "https://api.safetyculture.io"

class SafetyCultureAPI:
    """SafetyCulture API client."""

    def __init__(self, max_concurrent_requests=20):
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }
        self.max_concurrent_requests = max_concurrent_requests
        self.session = None
        self.semaphore = None

    async def __aenter__(self):
        # Create session with connection pooling
        connector = aiohttp.TCPConnector(
            limit=100,  # Total connection pool size
            limit_per_host=30,  # Max connections per host
            ttl_dns_cache=300,  # DNS cache TTL
            use_dns_cache=True,
        )
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            connector=connector,
            timeout=timeout
        )
        self.semaphore = asyncio.Semaphore(self.max_concurrent_requests)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_page(self, url: str) -> Dict:
        """Fetch a single page from the API with rate limiting"""
        async with self.semaphore:
            try:
                async with self.session.get(url) as response:
                    response.raise_for_status()
                    return await response.json()
            except asyncio.TimeoutError:
                print(f"⚠️  Timeout for URL: {url}")
                raise
            except Exception as e:
                print(f"❌ Error fetching {url}: {e}")
                raise

    async def fetch_all_data_optimized(self, initial_url: str, data_type: str) -> List[Dict]:
        """Optimized fetching with concurrent pagination and batching"""
        print(f"🚀 Starting optimized {data_type} fetch...")
        all_data = []

        # Use a queue to manage URLs to fetch
        url_queue = asyncio.Queue()
        await url_queue.put(initial_url)

        fetched_urls = set()
        page_count = 0
        batch_size = 15  # Fetch 15 pages concurrently

        while not url_queue.empty():
            # Collect URLs for current batch
            current_batch = []
            for _ in range(min(batch_size, url_queue.qsize())):
                if not url_queue.empty():
                    url = await url_queue.get()
                    if url not in fetched_urls:
                        current_batch.append(url)
                        fetched_urls.add(url)

            if not current_batch:
                break

            page_count += len(current_batch)
            print(f"  ⚡ Fetching batch of {len(current_batch)} pages (total pages: {page_count})")

            batch_start = time.time()

            # Fetch current batch concurrently
            tasks = [self.fetch_page(url) for url in current_batch]
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            batch_time = time.time() - batch_start
            batch_count = 0

            # Process responses and queue next pages
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    print(f"    ❌ Error in page {i+1}: {response}")
                    continue

                data = response.get('data', [])
                all_data.extend(data)
                batch_count += len(data)

                # Queue next page if it exists
                metadata = response.get('metadata', {})
                next_url = metadata.get('next_page')
                if next_url:
                    if not next_url.startswith('http'):
                        next_url = f"{BASE_URL}{next_url}"
                    if next_url not in fetched_urls:
                        await url_queue.put(next_url)

            remaining_in_queue = url_queue.qsize()
            total_records = len(all_data)
            rate = len(current_batch) / batch_time if batch_time > 0 else 0

            print(f"    ✅ Batch completed: {batch_count} records in {batch_time:.1f}s ({rate:.1f} pages/sec)")
            print(f"    📊 Total: {total_records:,} records, {remaining_in_queue} pages queued")

        print(f"🎉 Completed {data_type} fetch: {len(all_data):,} total records from {page_count} pages")
        return all_data

    async def fetch_all_inspections(self) -> List[Dict]:
        """Fetch all inspections with concurrent pagination"""
        initial_url = f"{BASE_URL}/feed/inspections?archived=false&completed=both"
        return await self.fetch_all_data_optimized(initial_url, "inspection")

    async def fetch_all_sites(self) -> List[Dict]:
        """Fetch all sites with concurrent pagination (only leaf nodes, not deleted)"""
        initial_url = f"{BASE_URL}/feed/sites?include_deleted=false&show_only_leaf_nodes=true"
        return await self.fetch_all_data_optimized(initial_url, "site")

def get_sites_with_activity(inspections: List[Dict]) -> Set[str]:
    """Extract unique site IDs that have inspection activity"""
    sites_with_activity = set()

    for inspection in inspections:
        site_id = inspection.get('site_id')
        if site_id:
            sites_with_activity.add(site_id)

    print(f"🎯 Found {len(sites_with_activity)} unique sites with inspection activity")
    return sites_with_activity

def find_sites_without_activity(sites: List[Dict], sites_with_activity: Set[str]) -> List[Dict]:
    """Find sites that don't have any inspection activity"""
    sites_without_activity = []

    for site in sites:
        site_id = site.get('id')  # Sites use 'id' field
        if site_id and site_id not in sites_with_activity:
            sites_without_activity.append(site)

    print(f"📊 {len(sites_without_activity)} out of {len(sites)} sites have no inspection activity")
    return sites_without_activity

def write_csv(data: List[Dict], filename: str):
    """Write data to CSV file"""
    if not data:
        print(f"⚠️  No data to write to {filename}")
        return

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    print(f"💾 Saved {len(data)} records to {filename}")

async def main():
    """Main execution function"""
    if not TOKEN:
        print("❌ Error: SAFETYCULTURE_TOKEN environment variable not set")
        print("Please set your token: export SAFETYCULTURE_TOKEN='your_token_here'")
        return

    print("🚀 Starting SafetyCulture Sites Without Activity Analysis (High Performance Mode)")
    print("=" * 80)

    start_time = datetime.now()

    async with SafetyCultureAPI(max_concurrent_requests=25) as api:
        # Fetch both inspections and sites concurrently
        print("🔄 Fetching inspections and sites concurrently...")

        fetch_start = time.time()
        inspections_task = asyncio.create_task(api.fetch_all_inspections())
        sites_task = asyncio.create_task(api.fetch_all_sites())

        # Wait for both to complete
        inspections, sites = await asyncio.gather(inspections_task, sites_task)
        fetch_time = time.time() - fetch_start

        print(f"⚡ Total fetch time: {fetch_time:.1f} seconds")

    print("\n📈 Processing data...")
    process_start = time.time()

    # Get sites that have inspection activity
    sites_with_activity = get_sites_with_activity(inspections)

    # Find sites without activity
    sites_without_activity = find_sites_without_activity(sites, sites_with_activity)
    process_time = time.time() - process_start

    # Generate timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "output"

    # Write results to CSV files
    print("\n💾 Saving results...")
    save_start = time.time()
    write_csv(sites_without_activity, f"{output_dir}/sites_without_activity_{timestamp}.csv")
    write_csv(inspections, f"{output_dir}/all_inspections_{timestamp}.csv")
    write_csv(sites, f"{output_dir}/all_sites_{timestamp}.csv")
    save_time = time.time() - save_start

    # Summary
    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "=" * 80)
    print("📋 PERFORMANCE SUMMARY")
    print("=" * 80)
    print(f"🏢 Total Sites: {len(sites):,}")
    print(f"🔍 Total Inspections: {len(inspections):,}")
    print(f"🎯 Sites with Activity: {len(sites_with_activity):,}")
    print(f"⚪ Sites without Activity: {len(sites_without_activity):,}")
    print(f"📊 Percentage without Activity: {(len(sites_without_activity)/len(sites)*100):.1f}%")
    print("\n🚀 TIMING BREAKDOWN:")
    print(f"  🏁 API Fetching: {fetch_time:.1f}s ({(len(inspections)+len(sites))/fetch_time:.0f} records/sec)")
    print(f"  📊 Data Processing: {process_time:.1f}s")
    print(f"  💾 File Saving: {save_time:.1f}s")
    print(f"  ⏱️  Total Runtime: {duration.total_seconds():.1f}s")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())