import random
from datetime import datetime, timedelta
import requests

# **** ENSURE YOU HAVE THE "WEB TASKS LINK TEMPLATES" FEATURE FLAG ENABLED VIA DEVELOPER TOOLS/PERISCOPE ***

COUNT = 100000  # Number of assets/actions/schedules you want to create

TOKEN = ''
GROUP_ID = ''  # Assignee. Just a single group to make testing easy (role_ or uuid)
TEMPLATE_ID = ''  # For schedules/recurring actions. Just a single template to make testing easy (must be uuid)
SCHEDULE_ID = ''  # For recurring actions - not transferrable across environments
# *** In order to obtain schedule id, create a recurring action via the front-end with your desired cadence. Then perform a get on that action item and you'll find a schedule id in "references".
CUSTOM_TYPE_ID = ''  # Not required

def get_types():
    url = "https://api.safetyculture.io/assets/v1/types/list"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.post(url, headers=headers)
    next_page = response.json().get('next_page_token', None)
    types = response.json()['type_list']
    while next_page:
        url = f"https://api.safetyculture.io/assets/v1/types/list?next_page_token={next_page}"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }

        response = requests.post(url, headers=headers)
        additional = response.json()['type_list']
        types.extend(additional)
        next_page = response.json().get('next_page_token', None)
    return types

def get_sites():
    url = "https://api.safetyculture.io/feed/sites?include_deleted=false&show_only_leaf_nodes=true"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(url, headers=headers)
    sites = response.json()['data']
    next_page = response.json()['metadata'].get('next_page', None)

    while next_page:
        url = f'https://api.safetyculture.io{next_page}'

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }
        response = requests.get(url, headers=headers)
        additional = response.json()['data']
        sites.extend(additional)
        next_page = response.json()['metadata'].get('next_page', None)
    return sites

def rand_type():
    types = get_types()
    types_index = random.randint(1, len(types)-1)
    type_item = types[types_index]  # Changed variable name to avoid shadowing 'type'
    return type_item

def rand_site():
    sites = get_sites()
    sites_index = random.randint(0, len(sites)-1)
    site = sites[sites_index]
    return site

def rand_priority():
    priorities = ['16ba4717-adc9-4d48-bf7c-044cfe0d2727', 'ce87c58a-eeb2-4fde-9dc4-c6e85f1f4055', '02eb40c1-4f46-40c5-be16-d32941c96ec9']
    priority_index = random.randint(0,2)
    priority = priorities[priority_index]
    return priority

def last_day_of_month():
    now = datetime.now() + timedelta(hours=6)
    next_month = now.replace(day=28) + timedelta(days=4)
    raw = next_month - timedelta(days=next_month.day)
    clean = raw.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return clean

def create_asset(type_item, site):
    uniq = random.randint(100000000, 999999999)
    code = f'{uniq} - {type_item["name"]} - TEST'

    url = "https://api.safetyculture.io/assets/v1/assets"

    payload = {
        "site": site,
        "code": code,
        "type_id": type_item['id']
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.post(url, json=payload, headers=headers)
    asset_id = response.json()['id']

    return {
        "asset_id": asset_id,
        "code": code,
        "site": site
    }

def create_action(asset):
    priority = rand_priority()
    creat_raw = datetime.now() + timedelta(hours=6)
    created = creat_raw.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    due = last_day_of_month()
    title = asset['code']
    site = asset['site']
    asset_id = asset['asset_id']

    url = "https://api.safetyculture.io/tasks/v1/actions"

    if CUSTOM_TYPE_ID == '':
        payload = {
            "title": title,
            "description": "Mark action complete if Pass, Start an inspection if you see deficiencies.",
            "collaborators": [
                {
                    "collaborator_type": "GROUP",
                    "assigned_role": "ASSIGNEE",
                    "group": { "group_id": GROUP_ID },
                    "collaborator_id": GROUP_ID
                }
            ],
            "priority_id": priority,
            "status_id": "17e793a1-26a3-4ecd-99ca-f38ecc6eaa2e",
            "created_at": created,
            "due_at": due,
            "site_id": site,
            "references": [
                {
                    "type": "SCHEDULE",
                    "schedule_context": { "frequency": "FREQ=MONTHLY;BYMONTHDAY=1" },
                    "id": SCHEDULE_ID
                }
            ],
            "asset_id": asset_id
        }
    else:
        payload = {
            "type": {
                "type": "TASK_TYPE_CUSTOM",
                "id": CUSTOM_TYPE_ID
            },
            "title": title,
            "description": "Mark action complete if Pass, Start an inspection if you see deficiencies.",
            "collaborators": [
                {
                    "collaborator_type": "GROUP",
                    "assigned_role": "ASSIGNEE",
                    "group": { "group_id": GROUP_ID },
                    "collaborator_id": GROUP_ID
                }
            ],
            "priority_id": priority,
            "status_id": "17e793a1-26a3-4ecd-99ca-f38ecc6eaa2e",
            "created_at": created,
            "due_at": due,
            "site_id": site,
            "references": [
                {
                    "type": "SCHEDULE",
                    "schedule_context": { "frequency": "FREQ=MONTHLY;BYMONTHDAY=1" },
                    "id": SCHEDULE_ID
                }
            ],
            "asset_id": asset_id
        }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }
    response = requests.post(url, json=payload, headers=headers)
    action_id = response.json()['action_id']
    return action_id

def link_template(action_id):
    url = f"https://api.safetyculture.io/tasks/v1/tasks/{action_id}/link_template"

    payload = {
        "template_ids": [
            TEMPLATE_ID
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response

def create_schedule(asset):
    title = asset['code']
    site = asset['site']
    asset_id = asset['asset_id']
    now = datetime.now()
    first_day = now.replace(day=1)
    dtstart = first_day.strftime("%Y%m%dT%H%M%SZ")

    url = "https://api.safetyculture.io/schedules/v1/schedule_items"

    payload = {
        "must_complete": "ONE",
        "can_late_submit": True,
        "start_time": {
            "hour": 8,
            "minute": 0
        },
        "document": {
            "type": "TEMPLATE",
            "id": TEMPLATE_ID
        },
        "status": "ACTIVE",
        "description": title,
        "recurrence": f"FREQ=MONTHLY;BYDAY=MO;INTERVAL=1;DTSTART={dtstart}",
        "duration": "P1M",
        "assignees": [
            {
                "type": "ROLE",
                "id": GROUP_ID
            }
        ],
        "location_id": site,
        "asset_id": asset_id
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.post(url, json=payload, headers=headers)
    id_val = response.json().get('id', None)
    if id_val:
        return id_val
    return response.json()  # Removed else and simplified return

def main():
    count = COUNT
    while count > 0:
        site = rand_site()['site_uuid']
        type_item = rand_type()  # Changed to match the function return variable
        asset = create_asset(type_item, site)

        if random.randint(0,1) == 0: #if 0, then create an action. Otherwise, create a schedule
            action = create_action(asset)
            link_template(action)
            print(f"Action Item - {action}, {count} Remaining")
        else:
            schedule = create_schedule(asset)
            print(f"Schedule - {schedule}, {count} Remaining")
        count -= 1

main()
