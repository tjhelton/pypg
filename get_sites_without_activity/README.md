# Get Sites Without Activity

Identifies SafetyCulture sites with no inspection activity via API. Compares all sites against inspection records using concurrent processing.

## Quick Start

1. **Install dependencies**: `pip install requests`
2. **Set environment variable**: `export SAFETYCULTURE_TOKEN="your_api_token_here"`
3. **Run script**: `python main.py`
4. **Check output**: Find timestamped CSV files in `output/` directory

## Prerequisites

- Python 3.7+ and pip
- Valid SafetyCulture API token (environment variable)
- API access to inspections and sites feeds

## Input Format

No input file required - fetches all organizational data using environment variable for authentication.

## Output

Creates timestamped CSV files in `output/` directory:
- `sites_without_activity_YYYYMMDD_HHMMSS.csv`: Sites with no inspection activity
- `all_inspections_YYYYMMDD_HHMMSS.csv`: Complete inspections data
- `all_sites_YYYYMMDD_HHMMSS.csv`: Complete sites data

## API Reference

- Endpoints: `/feed/inspections`, `/feed/sites`
- [Documentation](https://developer.safetyculture.com/reference/)

## Notes

- Uses ThreadPoolExecutor for concurrent data fetching
- Processes only leaf node sites (excludes deleted)
- Provides detailed console logging with progress tracking