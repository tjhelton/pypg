# Get Sites Without Activity

This script identifies sites in SafetyCulture that have no inspection activity by comparing all sites against inspection records.

## What it does

1. **Fetches all inspections** from the organization (non-archived, both completed and incomplete)
2. **Fetches all sites** (only leaf nodes, excluding deleted sites)
3. **Extracts unique site IDs** from inspections to identify sites with activity
4. **Compares the lists** to find sites without any inspection activity
5. **Outputs results** to CSV files with live console logging

## Features

- ⚡ **Concurrent processing** using ThreadPoolExecutor for maximum efficiency
- 📄 **Automatic pagination** handling for large datasets
- 📊 **Live progress logging** with detailed console output
- 💾 **CSV export** of all results with timestamps
- 🔒 **Environment variable** support for secure token handling

## Requirements

- Python 3.7+
- requests
- concurrent.futures (built-in)
- csv (built-in)
- os (built-in)

## Installation

```bash
pip install requests
```

## Usage

1. Set your SafetyCulture API token as an environment variable:
   ```bash
   export SAFETYCULTURE_TOKEN="your_api_token_here"
   ```

2. Run the script:
   ```bash
   python main.py
   ```

## Output Files

The script creates timestamped CSV files in an `output/` directory:

- `sites_without_activity_YYYYMMDD_HHMMSS.csv` - Sites with no inspection activity
- `all_inspections_YYYYMMDD_HHMMSS.csv` - All inspections data
- `all_sites_YYYYMMDD_HHMMSS.csv` - All sites data

## API Endpoints Used

- `/feed/inspections?archived=false&completed=both` - All non-archived inspections
- `/feed/sites?include_deleted=false&show_only_leaf_nodes=true` - All active leaf node sites

## Performance

The script uses ThreadPoolExecutor to efficiently handle:
- Concurrent fetching of inspections and sites
- Automatic pagination through large datasets
- Memory-efficient processing of results

## Example Output

```
🚀 Starting SafetyCulture Sites Without Activity Analysis
============================================================
🔄 Fetching data concurrently...
🔍 Fetching inspections...
  📄 Page 1 - 1000 inspections - 1000 total - 2500 remaining
  📄 Page 2 - 1000 inspections - 2000 total - 1500 remaining
✅ Fetched 3500 total inspections

🏢 Fetching sites...
  📄 Page 1 - 1000 sites - 1000 total - 500 remaining
✅ Fetched 1500 total sites

📈 Processing data...
🎯 Found 850 unique sites with inspection activity
📊 650 out of 1500 sites have no inspection activity

💾 Saving results...
💾 Saved 650 records to output/sites_without_activity_20241215_143022.csv

============================================================
📋 SUMMARY
============================================================
🏢 Total Sites: 1500
🔍 Total Inspections: 3500
🎯 Sites with Activity: 850
⚪ Sites without Activity: 650
📊 Percentage without Activity: 43.3%
⏱️  Total Runtime: 12.5 seconds
============================================================
```