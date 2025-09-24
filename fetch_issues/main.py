#!/usr/bin/env python3
"""
SafetyCulture Issues Extractor
Fetches all issues with assignees and completion tracking from SafetyCulture API.
Outputs CSV with detailed issue information including who marked each issue complete.
"""

import asyncio
import os
import random
import time
import traceback
from datetime import datetime
from typing import List, Optional

import aiohttp
import pandas as pd

# Configuration
SC_API_BASE_URL = "https://api.safetyculture.io"
SC_API_TOKEN = os.getenv("SC_API_TOKEN")


class IssuesExtractor:  # pylint: disable=too-many-instance-attributes
    """Class to extract issues from SafetyCulture API."""

    def __init__(self, output_dir: str = "."):
        """Initialize the issues extractor."""
        self.output_dir = output_dir
        self.api_base_url = SC_API_BASE_URL
        self.api_token = SC_API_TOKEN

        # Data containers
        self.issues_data = []
        self.timeline_data = []
        self.assignees_data = []

        # Async settings
        self.max_concurrent_requests = 10
        self.batch_size = 1000

        # Retry configuration
        self.max_retries = 3
        self.base_delay = 2
        self.max_delay = 30

    async def get_session_headers(self):
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    async def retry_async_call(self, func, *args, **kwargs):
        """Retry an async API call with exponential backoff."""
        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:  # pylint: disable=broad-exception-caught
                if attempt == self.max_retries - 1:
                    print(f"Final async attempt failed: {e}")
                    raise

                delay = min(
                    self.base_delay * (2**attempt) + random.uniform(0, 1),
                    self.max_delay,
                )
                print(
                    f"Async API call failed (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
                print(f"Retrying in {delay:.1f} seconds...")
                await asyncio.sleep(delay)

    async def fetch_single_page(
        self, session: aiohttp.ClientSession, url: str, params: dict = None
    ) -> dict:
        """Fetch a single page of data from API with retry logic."""

        async def make_request():
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()

        try:
            return await self.retry_async_call(make_request)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error fetching {url} after all retries: {e}")
            return {"data": [], "metadata": {}}

    async def fetch_feed_chain(
        self, session: aiohttp.ClientSession, endpoint: str, params: dict = None
    ) -> List[dict]:
        """Fetch all data from a feed endpoint following next_page chain."""
        all_data = []
        current_url = f"{self.api_base_url}{endpoint}"
        page_count = 0

        print(f"Fetching data from {endpoint}...")

        while current_url:
            request_params = (
                params if current_url == f"{self.api_base_url}{endpoint}" else None
            )

            data = await self.fetch_single_page(session, current_url, request_params)
            items = data.get("data", [])

            if not items:
                break

            all_data.extend(items)
            page_count += 1

            metadata = data.get("metadata", {})
            next_page = metadata.get("next_page", "")
            remaining = metadata.get("remaining_records", 0)

            print(
                f"Fetched {endpoint} page {page_count}: {len(items)} items "
                f"(total: {len(all_data)}, remaining: {remaining})"
            )

            if next_page:
                current_url = f"{self.api_base_url}{next_page}"
            else:
                break

        print(
            f"Completed {endpoint}: {len(all_data)} total items in {page_count} pages"
        )
        return all_data

    async def fetch_all_data_concurrent(self):
        """Fetch issues, timeline items, and assignees concurrently."""
        print("Starting concurrent data fetch...")
        start_time = time.time()

        headers = await self.get_session_headers()
        timeout = aiohttp.ClientTimeout(total=300)

        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            tasks = [
                self.fetch_feed_chain(session, "/feed/issues"),
                self.fetch_feed_chain(session, "/feed/issue_timeline_items"),
                self.fetch_feed_chain(session, "/feed/issue_assignees"),
            ]

            self.issues_data, self.timeline_data, self.assignees_data = (
                await asyncio.gather(*tasks)
            )

        fetch_time = time.time() - start_time
        print(f"\nConcurrent fetch completed in {fetch_time:.2f} seconds")
        print(f"- Issues: {len(self.issues_data)}")
        print(f"- Timeline items: {len(self.timeline_data)}")
        print(f"- Assignees: {len(self.assignees_data)}")

    def find_completion_user(self, task_id: str) -> tuple[Optional[str], Optional[str]]:
        """Find the user who marked the issue as complete via timeline data.

        Returns:
            tuple: (user_id, user_name) or (None, None) if not found
        """
        # Look for status update events that likely represent completion
        status_events = [
            item
            for item in self.timeline_data
            if (
                item.get("task_id") == task_id
                and item.get("item_type") == "TASK_STATUS_UPDATED"
            )
        ]

        if status_events:
            # Sort by timestamp to get the most recent status change
            status_events.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            # Return both creator ID and name from the most recent status change
            latest_status_change = status_events[0]
            creator_id = latest_status_change.get("creator_id", "")
            creator_name = latest_status_change.get("creator_name", "")
            return creator_id, creator_name

        return None, None

    def get_assignee_names(self, task_id: str) -> str:
        """Get comma-separated list of assignee names for a task."""
        task_assignees = [
            item for item in self.assignees_data if item.get("issue_id") == task_id
        ]

        assignee_names = []
        for assignee in task_assignees:
            assignee_type = assignee.get("type", "")
            if assignee_type == "group":
                # For groups, look for group name or use name field
                group_name = assignee.get("group_name", assignee.get("name", ""))
                if group_name:
                    assignee_names.append(group_name)
            elif assignee_type == "user":
                # For users, use the name field directly
                user_name = assignee.get("name", "")
                if user_name:
                    assignee_names.append(user_name)

        return ", ".join(filter(None, assignee_names))

    def create_creator_name(self, issue: dict) -> str:
        """Create full creator name from available creator information."""
        # Try creator_user_name first (direct field)
        creator_name = issue.get("creator_user_name", "")
        if creator_name:
            return creator_name.strip()

        # Fallback to nested creator object
        creator = issue.get("creator", {})
        if isinstance(creator, dict):
            first_name = creator.get("firstname", "")
            last_name = creator.get("lastname", "")
            full_name = f"{first_name} {last_name}".strip()
            if full_name:
                return full_name
            # Try name field as fallback
            return creator.get("name", "").strip()

        return ""

    def process_issues_to_csv(self) -> pd.DataFrame:
        """Process all issues data into the required CSV format."""
        print("Processing issues data...")

        processed_issues = []

        for issue in self.issues_data:
            try:
                # Handle both task_id and id fields
                task_id = issue.get("task_id", issue.get("id", ""))

                # Get basic issue information
                creator_user_id = issue.get("creator_id", "")
                creator_name = self.create_creator_name(issue)

                title = issue.get("title", "")
                description = issue.get("description", "")
                created_at = issue.get("created_at", "")
                due_at = issue.get("due_at", "") or ""  # Handle null values
                completed_at = issue.get("completed_at", "") or ""
                unique_id = issue.get("unique_id", "")

                # Get status information (status is a string in the actual API)
                status_label = issue.get("status", "")

                # Get assignee names
                assignee_names = self.get_assignee_names(task_id)

                # Find who marked it complete
                completion_user_id, completion_user_name = self.find_completion_user(
                    task_id
                )

                processed_issue = {
                    "task_id": task_id,
                    "creator.user_id": creator_user_id,
                    "creator.name": creator_name,
                    "title": title,
                    "description": description,
                    "created_at": created_at,
                    "due_at": due_at,
                    "assignee_names": assignee_names,
                    "completed_at": completed_at,
                    "status.label": status_label,
                    "unique_id": unique_id,
                    "user_who_marked_complete.user_id": completion_user_id or "",
                    "user_who_marked_complete.name": completion_user_name or "",
                }

                processed_issues.append(processed_issue)

            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Error processing issue {issue.get('task_id', 'unknown')}: {e}")
                continue

        df = pd.DataFrame(processed_issues)
        print(f"Processed {len(df)} issues successfully")
        return df

    def export_raw_feeds_to_csv(self) -> str:
        """Export all raw feed data to timestamped CSV files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(self.output_dir, f"issues_export_{timestamp}")

        # Create timestamped output directory
        os.makedirs(output_dir, exist_ok=True)
        print(f"Created output directory: {output_dir}")

        # Export raw issues data
        if self.issues_data:
            issues_file = os.path.join(output_dir, "raw_issues.csv")
            issues_df = pd.DataFrame(self.issues_data)
            issues_df.to_csv(issues_file, index=False, encoding="utf-8")
            print(f"Exported {len(issues_df)} raw issues to: raw_issues.csv")

        # Export raw timeline data
        if self.timeline_data:
            timeline_file = os.path.join(output_dir, "raw_timeline_items.csv")
            timeline_df = pd.DataFrame(self.timeline_data)
            timeline_df.to_csv(timeline_file, index=False, encoding="utf-8")
            print(
                f"Exported {len(timeline_df)} raw timeline items to: raw_timeline_items.csv"
            )

        # Export raw assignees data
        if self.assignees_data:
            assignees_file = os.path.join(output_dir, "raw_assignees.csv")
            assignees_df = pd.DataFrame(self.assignees_data)
            assignees_df.to_csv(assignees_file, index=False, encoding="utf-8")
            print(f"Exported {len(assignees_df)} raw assignees to: raw_assignees.csv")

        return output_dir

    def export_processed_issues_to_csv(self, df: pd.DataFrame, output_dir: str) -> str:
        """Export processed DataFrame to CSV file in the specified directory."""
        filename = "processed_issues.csv"
        filepath = os.path.join(output_dir, filename)

        df.to_csv(filepath, index=False, encoding="utf-8")
        print(f"Exported {len(df)} processed issues to: processed_issues.csv")
        return filepath

    async def run_extraction(self) -> str:
        """Run the complete issues extraction process."""
        print("SafetyCulture Issues Extractor")
        print("=" * 35)

        if not self.api_token:
            raise ValueError("SC_API_TOKEN environment variable is required")

        # Fetch all data
        await self.fetch_all_data_concurrent()

        # Export raw feeds to CSV
        print("\nExporting raw feed data...")
        output_dir = self.export_raw_feeds_to_csv()

        # Process to CSV format
        issues_df = self.process_issues_to_csv()

        # Export processed issues to CSV
        self.export_processed_issues_to_csv(issues_df, output_dir)

        print("\n✓ Issues extraction completed successfully!")
        print(f"  Issues processed: {len(issues_df)}")
        print(f"  Output directory: {output_dir}")
        print(f"  Raw issues: {len(self.issues_data)} records")
        print(f"  Raw timeline items: {len(self.timeline_data)} records")
        print(f"  Raw assignees: {len(self.assignees_data)} records")

        return output_dir


async def main():
    """Main async function."""
    try:
        extractor = IssuesExtractor()
        await extractor.run_extraction()
        return 0
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error during extraction: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(asyncio.run(main()))
