import time
import uuid
import requests
import pandas as pd
import os

TOKEN = ""

def read_csv():
    csv_df = pd.read_csv("assets.csv").fillna("")
    csv_array = csv_df.to_dict("records")
    return csv_array

def log_results(results_array):
    for row in results_array:
        action_id = row["action_id"]
        title = row["title"]
        status = row["status"]
        message = row["message"]
        asset_id = row["asset_id"]
        df = pd.DataFrame(
            {"action_id": [action_id], "asset_id": [asset_id], "title": [title], "status": [status], "message": [message]}
        )
        df.to_csv(
            "output.csv", mode="a", header=not os.path.exists("output.csv"), index=False
        )

def create_action(action):
    max_retries = 3
    delay = 5
    action_id = str(uuid.uuid4())
    title = action['title']
    description = action['description']
    group_uuid = action['assignee']
    site_id = action['site_uuid']
    asset_id = action['asset_id']
    label_id = action['label_id']
    rrule_freq = action['frequency'].replace('\\n', '\n')
    template_id = action['template_id']
    url = "https://api.safetyculture.io/tasks/v1/actions:CreateActionSchedule"
    payload = {
        "title": title,
        "description": description,
        "collaborators": [
            {
                "collaboratorId": group_uuid,
                "collaboratorType": "GROUP",
                "assignedRole": "ASSIGNEE",
                "group": {"groupId": group_uuid}
            }
        ],
        "priorityId": "16ba4717-adc9-4d48-bf7c-044cfe0d2727",
        "siteId": site_id,
        "assetId": asset_id,
        "labelIds": [label_id],
        "frequency": rrule_freq,
        "actionId": action_id,
        "type": {
            "type": "TASK_TYPE_CUSTOM",
            "id": "883123e8-8cec-4fda-a3f0-7bdfd2b305bb"
        },
        "templateIds": [template_id]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Successfully created action '{title}' for asset {asset_id}. Response: {response.status_code}")
            return [{
                "action_id": action_id,
                "title": title,
                "asset_id": asset_id,
                "status": "SUCCESS",
                "message": "N/A"
            }]
        except requests.exceptions.RequestException as e:
            print(f"Error creating action '{title}': {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                print("Max retries reached. Giving up.")
                print(payload)
                return [{
                    "action_id": action_id,
                    "title": title,
                    "asset_id": asset_id,
                    "status": "ERROR",
                    "message": f"ERROR - {str(e)}"
                }]

def main():
    actions = read_csv()
    total_actions = len(actions)
    print(f"Total actions to process: {total_actions}")
    for i, action in enumerate(actions, 1):
        print(f"Processing action {i}/{total_actions}: {action['title']}...")
        result = create_action(action)
        log_results(result)

main()
