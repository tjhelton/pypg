import requests
import csv
from datetime import datetime

TOKEN = 'TOKEN'

def create_action(action):
    url = "https://api.safetyculture.io/tasks/v1/actions"
    payload = {
        "title": action['title'],
        "description": action.get('description', ''),
        "priority_id": action.get('priority_id', ''),
        "status_id": action.get('status_id', ''),
        "created_at": action.get('created_at', ''),
        "due_at": action.get('due_at', ''),
        "inspection_id": action.get('inspection_id', ''),
        "inspection_item_id": action.get('inspection_item', ''),
        "template_id": action.get('template_id', ''),
        "site_id": action.get('site', ''),
        "asset_id": action.get('asset_id', '')
    }

    if action['collaborator_type']:
        payload["collaborators"] = [
            {
                "collaborator_type": action.get('collaborator_type', ''),
                "assigned_role": "ASSIGNEE",
                "collaborator_id": action.get('collaborator_id', '')
            }
        ]

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response

def main():
    log_entries = []
    with open('actions_to_transfer.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Attempt to create action
            response = create_action(row)
            if response.status_code == 200:
                status = "Success"
            else:
                status = f"Failed - Error {response.status_code}: {response.text[:100]}..."
            
            log_entries.append({
                "title": row['title'],
                "status": status,
                "response": response.text
            })
    
    # Write log entries to a new CSV file
    with open('action_creation_log.csv', mode='w', newline='') as file:
        fieldnames = ['title', 'status', 'response']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in log_entries:
            writer.writerow(entry)

if __name__ == "__main__":
    main()