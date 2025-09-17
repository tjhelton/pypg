# SafetyCulture Template Access Rules Export

Exports all permission assignments for each template in a SafetyCulture environment to CSV.

## Setup

1. Install dependencies: `pip install requests`
2. Edit `main.py` and add your API token:
   ```python
   TOKEN = 'your_actual_safetyculture_api_token'  # Add your API token here
   ```

## Usage

```bash
python main.py
```

Outputs to `template_access_rules.csv` with columns: template_id, name, permission, assignee_type, assignee_id, assignee_name