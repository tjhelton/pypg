# Fetch Issues

Fetches all SafetyCulture issues via API with detailed information including assignees and completion tracking. Uses concurrent processing for high-performance data extraction.

## Quick Start

1. **Install dependencies**: `pip install aiohttp asyncio pandas`
2. **Set API token**: Replace `TOKEN = ''` in `main.py` with your SafetyCulture API token
3. **Run script**: `python main.py`
4. **Check output**: Find timestamped directory with CSV files

## Prerequisites

- Python 3.8+ with asyncio support
- Valid SafetyCulture API token
- API access to issues, timeline items, and assignees

## Input Format

No input file required - fetches all issues from organization using API token configured in script.

## Output

Creates timestamped directory (e.g., `issues_export_20240923_143052/`) with:
- `raw_issues.csv`: Complete unprocessed issues data
- `raw_timeline_items.csv`: Status change tracking events
- `raw_assignees.csv`: Assignee relationship data
- `processed_issues.csv`: Final processed data with 13 required columns

## API Reference

- Endpoints: `/feed/issues`, `/feed/issue_timeline_items`, `/feed/issue_assignees`
- [Documentation](https://developer.safetyculture.com/reference/)

## Notes

- Uses async/await for concurrent API fetching
- Handles pagination and retry logic automatically
- Tracks completion events via timeline analysis
