# SafetyCulture Issues Extractor

Fetches all issues from SafetyCulture API with detailed information including assignees and completion tracking.

## Features

- **Concurrent API Fetching**: Uses async/await for high-performance data retrieval
- **Complete Issue Data**: Extracts all required fields including creator, assignees, and completion information
- **Timeline Tracking**: Identifies who marked each issue as complete via timeline analysis
- **Assignee Resolution**: Handles both user and group assignees with proper name formatting
- **CSV Export**: Generates timestamped CSV files with all required columns

## Required Columns in Output

The script exports CSV files with the following columns:

- `task_id` - Issue task ID
- `creator.user_id` - User ID of issue creator
- `creator.name` - Full name of issue creator (firstname + lastname)
- `title` - Issue title
- `description` - Issue description
- `created_at` - Issue creation timestamp
- `due_at` - Issue due date
- `assignee_names` - Comma-separated list of assignee names (users and groups)
- `completed_at` - Issue completion timestamp
- `status.label` - Current status label
- `unique_id` - Issue unique identifier
- `user_who_marked_complete.user_id` - User ID of person who marked issue complete
- `user_who_marked_complete.name` - Full name of person who marked issue complete

## Usage

### Prerequisites

Set your SafetyCulture API token as an environment variable:

```bash
export SC_API_TOKEN="your_api_token_here"
```

### Running the Script

```bash
# Navigate to the script directory
cd rcscripts/fetch_issues

# Run the extraction
python3 main.py
```

The script will:
1. Fetch all issues from SafetyCulture API
2. Fetch timeline items to track completion events
3. Fetch assignee information
4. Export raw feed data to CSV files
5. Process and correlate all data
6. Export processed data to CSV file

## Output Files

The script creates a timestamped directory (e.g., `issues_export_20240923_143052/`) containing:

### Raw Data Files
- `raw_issues.csv` - Complete unprocessed issues data from API
- `raw_timeline_items.csv` - All timeline events for status tracking
- `raw_assignees.csv` - Assignee relationship data

### Processed Data File
- `processed_issues.csv` - Final processed data with all required columns

## API Endpoints Used

- `/feed/issues` - Main issues data
- `/feed/issue_timeline_items` - Status change tracking
- `/feed/issue_assignees` - Assignee information

## Performance

The script uses concurrent async requests to maximize performance:
- Fetches multiple data types simultaneously
- Handles pagination automatically
- Implements retry logic with exponential backoff
- Typically processes thousands of issues in under a minute

## Error Handling

- Comprehensive retry logic for API calls
- Graceful handling of missing or malformed data
- Detailed logging of processing steps
- Continues processing even if individual records fail

## Output

Creates a timestamped CSV file in the same directory with all issue data ready for analysis or import into other systems.