# Export Template Access Rules

Exports all permission assignments for SafetyCulture templates via API. Fetches template access data and generates CSV output.

## Quick Start

1. **Install dependencies**: `pip install -r ../../requirements.txt`
2. **Set API token**: Replace `TOKEN = ''` in `main.py` with your SafetyCulture API token
3. **Run script**: `python main.py`
4. **Check output**: Find `template_access_rules.csv` file

## Prerequisites

- Python 3.8+ and pip
- Valid SafetyCulture API token
- API access to template permissions

## Input Format

No input file required - fetches all template access rules from organization.

## Output

Generates `template_access_rules.csv` with:
- `template_id`: Template identifier
- `name`: Template name
- `permission`: Permission level
- `assignee_type`: User or group assignment
- `assignee_id`: Assignee identifier
- `assignee_name`: Assignee display name

## API Reference

- Endpoint: Template permissions API
- [Documentation](https://developer.safetyculture.com/reference/)

## Notes

- Exports complete permission matrix for all templates
- Useful for access auditing and compliance
- Keep API tokens secure
