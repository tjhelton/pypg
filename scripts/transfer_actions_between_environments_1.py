import csv
import requests

# Note: The import of 'json' was removed since it's not used in the provided code.

OLD_TOKEN = 'TOKEN'
NEW_TOKEN = 'TOKEN'

def feed_actions():
    url = 'https://api.safetyculture.io/feed/actions'
    headers = {'authorization': f'Bearer {OLD_TOKEN}', 'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    data = response.json()['data']
    action_ids = [row['id'] for row in data]
    return action_ids

def get_action(action_id):
    url = f'https://api.safetyculture.io/tasks/v1/actions/{action_id}?modified_after'
    headers = {'authorization': f'Bearer {OLD_TOKEN}', 'accept': 'application/json'}
    response = requests.get(url, headers=headers)

    response.raise_for_status()

    full_action = response.json().get('action', {}).get('task', {})

    if full_action.get('collaborators') and len(full_action['collaborators']) > 0:
        collaborator = full_action['collaborators'][0]
        coll_type = collaborator.get('collaborator_type', '')
        coll_id = collaborator.get('user', {}).get('user_id', '') or collaborator.get('group', {}).get('group_id', '')
    else:
        coll_type = ''
        coll_id = ''

    temp_id = full_action.get('template_id', '')
    inspection_id = full_action.get('inspection', {}).get('inspection_id', '')
    inspection_item_id = full_action.get('inspection_item', {}).get('inspection_item_id', '')
    site_id = full_action.get('site', {}).get('id', '')

    return {
        'task_id': full_action.get('task_id', ''),
        'title': full_action.get('title', ''),
        'description': full_action.get('description', ''),
        'created_at': full_action.get('created_at', ''),
        'due_at': full_action.get('due_at', ''),
        'priority_id': full_action.get('priority_id', ''),
        'status_id': full_action.get('status_id', ''),
        'collaborator_type': coll_type,
        'collaborator_id': coll_id,
        'template_id': temp_id,
        'inspection_id': inspection_id,
        'inspection_item': inspection_item_id,
        'site': site_id,
        'completed_at': full_action.get('completed_at', ''),
        'status': full_action.get('status', {}).get('status_id', ''),
        'asset_id': full_action.get('asset_id', ''),
    }

def get_new_user(old_id):
    get_url = f"https://api.safetyculture.io/users/{old_id}"
    get_headers = {"accept": "application/json", "authorization": f"Bearer {OLD_TOKEN}"}
    get_response = requests.get(get_url, headers=get_headers)
    email = get_response.json()['email']

    search_url = "https://api.safetyculture.io/users/search"
    search_payload = {"email": [email]}
    search_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {NEW_TOKEN}"
    }
    search_response = requests.post(search_url, json=search_payload, headers=search_headers)
    new_user = search_response.json()['users']
    if new_user:
        new_id = new_user[0].get('id', '')
    else:
        new_id = ''
    return new_id

def list_new_groups():
    url = "https://api.safetyculture.io/groups"
    headers = {"accept": "application/json", "authorization": f"Bearer {NEW_TOKEN}"}
    response = requests.get(url, headers=headers)
    groups = response.json()['groups']
    return groups

def list_old_groups():
    url = "https://api.safetyculture.io/groups"
    headers = {"accept": "application/json", "authorization": f"Bearer {OLD_TOKEN}"}
    response = requests.get(url, headers=headers)
    groups = response.json()['groups']
    return groups

def get_new_group(old_id):
    new_groups = list_new_groups()
    old_groups = list_old_groups()
    old_name = next((row['name'] for row in old_groups if row['id'] == old_id), None)
    new_id = next((row['id'] for row in new_groups if row['name'] == old_name), None)
    return new_id

def enrich_records(actions):
    enriched = []
    for row in actions:
        if row['collaborator_type'] == 'USER':
            old_id = row['collaborator_id']
            new_id = get_new_user(old_id)
        elif row['collaborator_type'] == 'GROUP':
            old_id = row['collaborator_id']
            new_id = get_new_group(old_id)
        else:
            new_id = ''
        enriched.append({
            'task_id': row.get('task_id', ''),
            'title': row.get('title', ''),
            'description': row.get('description', ''),
            'created_at': row.get('created_at', ''),
            'due_at': row.get('due_at', ''),
            'priority_id': row.get('priority_id', ''),
            'status_id': row.get('status_id', ''),
            'collaborator_type': row.get('collaborator_type', ''),
            'collaborator_id': new_id,
            'template_id': row.get('template_id', ''),
            'inspection_id': row.get('inspection_id', ''),
            'inspection_item': row.get('inspection_item', ''),
            'site': row.get('site', ''),
            'completed_at': row.get('completed_at', ''),
            'status': row.get('status', ''),
            'asset_id': row.get('asset_id', ''),
        })
    return enriched

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
        "authorization": f"Bearer {NEW_TOKEN}"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text

def write_csv(logs):
    fieldnames = logs[0].keys()
    with open('action_transfer_log.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(logs)

def main():
    non_enriched = []
    err_log = []
    action_ids = feed_actions()
    for row in action_ids:
        non_enriched.append(get_action(row))
    enriched = enrich_records(non_enriched)
    for row in enriched:
        response = create_action(row)
        err_log.append({
            "action_id": row['task_id'],
            "response": response,
            "inspection": row['inspection_id']
        })
    write_csv(err_log)

main()