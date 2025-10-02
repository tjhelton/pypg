#!/usr/bin/env python3
"""
SafetyCulture Asset Archive Script

This script reads asset UUIDs from an input CSV file and archives them in SafetyCulture
using their API. It provides live logging of the archiving process to an output CSV file.

Usage:
    python delete_assets.py --api-token YOUR_API_TOKEN --input input.csv --output output.csv

Requirements:
    - pandas
    - requests
    - python-dotenv (optional, for environment variables)

API Endpoint: PATCH /assets/v1/assets/{id}/archive
"""

import argparse
import csv
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import requests

TOKEN = ""  # Add your SafetyCulture API token here

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SafetyCultureAssetArchiver:
    """
    A class to handle archiving of SafetyCulture assets via their API.
    """

    def __init__(self, api_token: str, base_url: str = "https://api.safetyculture.io"):
        """
        Initialize the SafetyCulture Asset Archiver.

        Args:
            api_token: SafetyCulture API token
            base_url: Base URL for SafetyCulture API
        """
        self.api_token = api_token
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # Statistics
        self.stats = {"total": 0, "successful": 0, "failed": 0, "skipped": 0}

    def archive_asset(self, asset_id: str) -> Dict[str, Any]:
        """
        Archive a single asset in SafetyCulture.

        Args:
            asset_id: UUID of the asset to archive

        Returns:
            Dictionary containing the result of the archive attempt
        """
        url = f"{self.base_url}/assets/v1/assets/{asset_id}/archive"

        # Archive request typically requires an empty body or specific parameters
        archive_data = {}

        try:
            logger.info(f"Attempting to archive asset: {asset_id}")
            response = self.session.patch(url, json=archive_data)

            result = {
                "asset_id": asset_id,
                "timestamp": datetime.now().isoformat(),
                "status_code": response.status_code,
                "success": False,
                "error_message": None,
                "response_body": None,
            }

            if response.status_code == 200:
                result["success"] = True
                result["response_body"] = (
                    response.text if response.text else "Asset archived successfully"
                )
                self.stats["successful"] += 1
                logger.info(f"Successfully archived asset: {asset_id}")
            else:
                result["error_message"] = (
                    f"HTTP {response.status_code}: {response.text}"
                )
                self.stats["failed"] += 1
                logger.error(
                    f"Failed to archive asset {asset_id}: {result['error_message']}"
                )

        except requests.exceptions.RequestException as e:
            result = {
                "asset_id": asset_id,
                "timestamp": datetime.now().isoformat(),
                "status_code": None,
                "success": False,
                "error_message": str(e),
                "response_body": None,
            }
            self.stats["failed"] += 1
            logger.error(f"Request exception for asset {asset_id}: {e}")

        except Exception as e:
            result = {
                "asset_id": asset_id,
                "timestamp": datetime.now().isoformat(),
                "status_code": None,
                "success": False,
                "error_message": f"Unexpected error: {str(e)}",
                "response_body": None,
            }
            self.stats["failed"] += 1
            logger.error(f"Unexpected error for asset {asset_id}: {e}")

        return result

    def read_asset_ids_from_csv(self, input_file: str) -> List[str]:
        """
        Read asset IDs from input CSV file with header row.

        Expected CSV format:
        asset_id
        abc123-def456-ghi789
        def456-ghi789-jkl012

        Args:
            input_file: Path to the input CSV file

        Returns:
            List of asset IDs
        """
        try:
            # Read CSV with pandas, expecting header row
            df = pd.read_csv(input_file)

            # Check for expected column name (case insensitive)
            asset_id_column = None
            for col in df.columns:
                if col.lower() in ["asset_id", "id", "uuid"]:
                    asset_id_column = col
                    break

            if asset_id_column is None:
                logger.error(
                    f"No valid asset ID column found. Expected 'asset_id', 'id', or 'uuid'. Found columns: {list(df.columns)}"
                )
                sys.exit(1)

            # Extract asset IDs and remove any empty/NaN values
            asset_ids = df[asset_id_column].dropna().astype(str).str.strip().tolist()

            # Remove any empty strings
            asset_ids = [aid for aid in asset_ids if aid]

            if not asset_ids:
                logger.error("No asset IDs found in the input file")
                sys.exit(1)

            logger.info(f"Read {len(asset_ids)} asset IDs from {input_file}")
            return asset_ids

        except FileNotFoundError:
            logger.error(f"Input file not found: {input_file}")
            sys.exit(1)
        except pd.errors.EmptyDataError:
            logger.error(f"Input file is empty: {input_file}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error reading input file: {e}")
            sys.exit(1)

    def write_result_to_csv(
        self, output_file: str, result: Dict[str, Any], write_header: bool = False
    ):
        """
        Write a single result to the output CSV file.

        Args:
            output_file: Path to the output CSV file
            result: Result dictionary to write
            write_header: Whether to write the CSV header
        """
        fieldnames = [
            "asset_id",
            "timestamp",
            "success",
            "status_code",
            "error_message",
            "response_body",
        ]

        try:
            file_exists = Path(output_file).exists()

            with open(output_file, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write header if file is new or write_header is True
                if not file_exists or write_header:
                    writer.writeheader()

                writer.writerow(result)
                csvfile.flush()  # Ensure data is written immediately

        except Exception as e:
            logger.error(f"Error writing to output file: {e}")

    def archive_assets_from_csv(
        self, input_file: str, output_file: str, delay: float = 0.1
    ):
        """
        Archive assets listed in CSV file and log results.

        Args:
            input_file: Path to input CSV file containing asset IDs
            output_file: Path to output CSV file for logging results
            delay: Delay in seconds between API calls (to respect rate limits)
        """
        # Read asset IDs
        asset_ids = self.read_asset_ids_from_csv(input_file)

        if not asset_ids:
            logger.warning("No asset IDs found in input file")
            return

        self.stats["total"] = len(asset_ids)

        # Initialize output file with header
        self.write_result_to_csv(output_file, {}, write_header=True)

        logger.info(f"Starting archiving of {len(asset_ids)} assets...")
        logger.info(f"Results will be logged to: {output_file}")

        start_time = time.time()

        for i, asset_id in enumerate(asset_ids, 1):
            logger.info(f"Processing asset {i}/{len(asset_ids)}: {asset_id}")

            # Archive the asset
            result = self.archive_asset(asset_id)

            # Write result to CSV immediately
            self.write_result_to_csv(output_file, result)

            # Add delay between requests to respect rate limits
            if delay > 0 and i < len(asset_ids):
                time.sleep(delay)

        end_time = time.time()
        duration = end_time - start_time

        # Log final statistics
        logger.info("=" * 50)
        logger.info("ARCHIVING SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Total assets processed: {self.stats['total']}")
        logger.info(f"Successfully archived: {self.stats['successful']}")
        logger.info(f"Failed archives: {self.stats['failed']}")
        logger.info(f"Skipped: {self.stats['skipped']}")
        logger.info(
            f"Success rate: {(self.stats['successful'] / self.stats['total']) * 100:.1f}%"
        )
        logger.info(f"Total time: {duration:.2f} seconds")
        logger.info(
            f"Average time per asset: {duration / self.stats['total']:.2f} seconds"
        )
        logger.info(f"Results logged to: {output_file}")


def main():
    """Main function to handle command line arguments and execute the archiving process."""
    parser = argparse.ArgumentParser(
        description="Archive SafetyCulture assets from CSV list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python delete_assets.py --api-token YOUR_TOKEN --input input.csv --output output.csv
  python delete_assets.py --api-token YOUR_TOKEN --input input.csv --output output.csv --delay 0.5

Environment Variables:
  SC_API_TOKEN - SafetyCulture API token (alternative to --api-token)
        """,
    )

    parser.add_argument(
        "--api-token",
        type=str,
        help="SafetyCulture API token (or set SC_API_TOKEN environment variable)",
    )

    parser.add_argument(
        "--input",
        type=str,
        default="input.csv",
        help="Input CSV file containing asset IDs (default: input.csv)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="archive_results.csv",
        help="Output CSV file for logging results (default: archive_results.csv)",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.1,
        help="Delay between API calls in seconds (default: 0.1)",
    )

    parser.add_argument(
        "--base-url",
        type=str,
        default="https://api.safetyculture.io",
        help="SafetyCulture API base URL (default: https://api.safetyculture.io)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without actually archiving assets",
    )

    args = parser.parse_args()

    # Get API token from args or environment
    api_token = TOKEN

    if not api_token:
        logger.error(
            "API token is required. Use --api-token or set SC_API_TOKEN environment variable."
        )
        sys.exit(1)

    # Validate input file exists
    if not Path(args.input).exists():
        logger.error(f"Input file does not exist: {args.input}")
        sys.exit(1)

    if args.dry_run:
        logger.info("DRY RUN MODE - No assets will actually be archived")
        # In dry run mode, just read and validate the input file
        archiver = SafetyCultureAssetArchiver(api_token, args.base_url)
        asset_ids = archiver.read_asset_ids_from_csv(args.input)
        logger.info(f"Dry run complete. Would archive {len(asset_ids)} assets.")
        return

    # Confirm before proceeding
    print("About to archive assets in SafetyCulture using:")
    print(f"  Input file: {args.input}")
    print(f"  Output file: {args.output}")
    print(f"  API base URL: {args.base_url}")
    print(f"  Delay between calls: {args.delay}s")

    confirmation = (
        input("\nAre you sure you want to proceed? (yes/no): ").lower().strip()
    )
    if confirmation not in ["yes", "y"]:
        logger.info("Operation cancelled by user")
        sys.exit(0)

    # Initialize archiver and start the process
    archiver = SafetyCultureAssetArchiver(api_token, args.base_url)

    try:
        archiver.archive_assets_from_csv(args.input, args.output, args.delay)
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
