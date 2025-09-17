# SafetyCulture Template Access Rules Export

This script exports all permission assignments for each template in a SafetyCulture environment. It generates a comprehensive CSV report showing individual permission assignments for every template, making it easy to audit and review access controls.

## Features

- **Complete Data Export**: Fetches all templates, users, and groups from SafetyCulture datafeeds
- **ID Transformation**: Automatically converts feed IDs to proper UUID format
- **Real-time CSV Writing**: Writes results as they're processed for progress monitoring
- **Permission Breakdown**: Creates individual rows for each permission assignment
- **Progress Logging**: Provides console output to track export progress
- **Error Handling**: Graceful handling of API errors and missing data

## Prerequisites

- Python 3.7 or higher
- `requests` library (`pip install requests`)
- SafetyCulture API token with appropriate permissions

## Required Permissions

Your SafetyCulture API token must have access to:
- Templates datafeed (`/feed/templates`)
- Users datafeed (`/feed/users`)
- Groups datafeed (`/feed/groups`)
- Template details endpoint (`/templates/v1/templates/{id}`)

## Setup

1. **Install Dependencies**:
   ```bash
   pip install requests
   ```

2. **Configure API Token**:
   Edit the `main.py` file and replace the token placeholder:
   ```python
   # Change this line in main.py:
   TOKEN = 'your_token_here'
   # To:
   TOKEN = 'your_actual_safetyculture_api_token'
   ```

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Fetch all users and groups (with progress logging)
2. Process each template to extract permission assignments
3. Write results to `template_access_rules.csv` in real-time

## Output Format

The generated CSV contains the following columns:

| Column | Description |
|--------|-------------|
| `template_id` | The unique identifier of the template |
| `name` | The name of the template |
| `permission` | The type of permission (`view`, `edit`, `delete`, `owner`, `context`) |
| `assignee_type` | Whether the assignee is a `user` or `group` |
| `assignee_id` | The UUID of the user or group |
| `assignee_name` | The display name of the user or group |

### Example Output

```csv
template_id,name,permission,assignee_type,assignee_id,assignee_name
template_123,Safety Inspection,view,user,6e628f05-4e90-4d5a-9692-535246beecb8,John Smith
template_123,Safety Inspection,edit,group,8a45b2c1-3d2e-4f5a-9b8c-7e6d5a4b3c2d,Safety Managers
template_456,Equipment Check,view,user,9f7e6d5c-4b3a-4829-8176-2e1d0c9b8a76,Jane Doe
```

## How It Works

### Data Collection Process

1. **Users Feed**: Fetches all users and transforms their IDs from format `role_6e628f054e904d5a9692535246beecb8` to proper UUID format `6e628f05-4e90-4d5a-9692-535246beecb8`

2. **Groups Feed**: Fetches all groups with the same ID transformation

3. **Templates Feed**: Fetches all templates (excluding archived ones)

4. **Template Details**: For each template, fetches detailed information including permissions

### ID Transformation

The script handles SafetyCulture's feed ID format transformation:
- **Input**: `role_6e628f054e904d5a9692535246beecb8`
- **Process**: Split on `_`, take second part, format as UUID
- **Output**: `6e628f05-4e90-4d5a-9692-535246beecb8`

### Permission Processing

For each template, the script:
- Extracts all permission types (`view`, `edit`, `delete`, `owner`, `context`)
- Creates individual rows for each user/group assignment
- Resolves user/group names using the lookup tables built from the feeds
- Handles both `USER` and `ROLE` (group) permission types

## Configuration

### Configuration Variables

| Variable | Location | Default | Description |
|----------|----------|---------|-------------|
| `TOKEN` | Line 24 in main.py | `'your_token_here'` | Your SafetyCulture API token |
| `BASE_URL` | Line 25 in main.py | `'https://api.safetyculture.io'` | SafetyCulture API base URL |

### Customization

You can modify the script to:
- Change the output filename (line 204: `output_file = 'template_access_rules.csv'`)
- Include archived templates (remove line 217: `if template_summary.get('archived', False): continue`)
- Add additional fields from the API responses
- Modify progress logging frequency (lines with `% 100`, `% 50`, `% 10`)

## Troubleshooting

### Common Issues

1. **Authentication Error**: Verify your `TOKEN` is correct and has the required permissions

2. **Rate Limiting**: The script includes basic error handling but doesn't implement retry logic. If you encounter rate limits, consider adding delays between requests.

3. **Large Datasets**: For organizations with many templates/users, the script may take time to complete. Progress is logged to the console.

4. **Missing Names**: If you see "Unknown User" or "Unknown Group", it means the user/group wasn't found in the feeds, possibly due to permissions or deleted accounts.

### Error Messages

- `Please set your SafetyCulture API token in the TOKEN variable`: Replace the placeholder token in the script
- `Error making request to {url}`: Check your network connection and API token permissions
- `Could not fetch template {id}`: The template may be deleted or you lack permissions

## Performance Notes

- The script processes data sequentially to avoid overwhelming the API
- CSV is written in real-time so you can monitor progress
- Memory usage is optimized by processing items as generators rather than loading all data at once
- Progress logging occurs at regular intervals (every 100 users, 50 groups, 10 templates)

## Security Considerations

- Store your API token securely and never commit it to version control
- The generated CSV may contain sensitive organizational data - handle appropriately
- Consider the least-privilege principle when generating API tokens

## License

This script is provided as-is for educational and operational purposes.