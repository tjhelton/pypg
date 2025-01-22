import requests
import random
from datetime import datetime, timedelta

# **** ENSURE YOU HAVE THE "WEB TASKS LINK TEMPLATES" FEATURE FLAG ENABLED VIA DEVELOPER TOOLS/PERISCOPE ***

COUNT = 50000 # Number of assets/actions/schedules you want to create

TOKEN = 'cabff0b948a30a1829b7c0ab1e00f20aadf2170c903316e702313d27bce243b7'
SCHEDULE_ID = '93b4cce9-9663-4ec6-900c-ff8ac73482f2' # For recurring actions - not transferrable across environments
# *** In order to obtain schedule id, create a recurring action via the front-end with your desired cadence. Then perform a get on that action item and you'll find a schedule id in "references". 
CUSTOM_TYPE_ID = '7d346223-e902-418d-8b9c-9064469eb7ac' # Not required

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
    type = types[types_index]
    return type

def rand_site():
    # sites = get_sites()
    sites = [
    "939a9b6b-5a89-4f23-b493-ba3a902308cc",
    "ab78c250-a5d2-4f23-b70a-001aa001726a",
    "8ff891b1-8035-42e8-b498-59c74e5fbee1",
    "6f541713-aca3-4a27-839d-f676f2c03b48",
    "6bae9267-0f2f-4280-992c-7464838bad55",
    "6979db7d-2c84-41cd-bb8e-1f773ecf1d86",
    "c06a14a1-09f2-4e5a-9d50-d0e14d65010f",
    "539a62b6-facc-4be2-b716-9b361f8cd5cb",
    "b8e48ca6-d27d-424b-9052-abed6ec560d3",
    "ac131f60-54fe-4835-aaf4-669fe132f4b5",
    "e6574c3b-0034-43f3-81ae-d074e1537cbc",
    "4cadc3ae-d0db-4d11-b71a-a90119069b50",
    "8a2a2224-0fa3-49a0-8053-aa6d07427638",
    "0cab954e-5da5-4df6-9ff4-cdd32837236b",
    "697e2bbe-a14e-4089-aa27-1648f634345a",
    "8b3232b5-86a1-47ff-a5ed-e50de286bade",
    "4147923d-1683-444c-ada1-871e92687146",
    "ce277160-3044-4cf8-b9d3-d281d80d6bc5",
    "7d08870a-03a0-41d7-9ba5-3f7d41fb32e7",
    "eba985c9-b1c4-461a-b72e-ba14ebf0d14c",
    "f1786407-b488-4d2e-bc3f-3350cf76c6cd",
    "60aec4fd-f475-466b-a1e9-f87a386ea62f",
    "98b3ec43-abed-4d82-8436-8b35cd12e795",
    "7ea9621c-9891-48b1-8fe9-bd396e7eba66",
    "788d4f29-c2a1-485a-909f-a26e560c6263",
    "c096c4a7-8099-422d-ac18-0c90908d05c3",
    "13b035dd-0578-4370-972a-ded835d53441",
    "325c8d50-26c9-416f-9a58-832c463ffeaf",
    "fa1ab1ac-ef4e-4ab9-bf26-f79016cbdd5d",
    "09d0d4b2-7b77-4174-b153-5fef5b050a06",
    "744cd2ba-0fd6-4437-97d6-cc3268c26b7b",
    "58ca7b0d-fcea-4411-8f2a-0009c6565318",
    "a0a4bc83-edf8-4bcb-bdc1-c56123363f36",
    "433793e8-bdcb-47d5-b2c9-15403285ac1a",
    "6603a219-5c3a-4bea-a77e-235f57b42f73",
    "def517a7-e19e-4224-a94d-ed264368c522",
    "3a1d981a-26b4-4168-9612-632350a866ce",
    "14b1a61c-c482-42f6-8ffa-ecaeae46072d",
    "7801998a-1971-4007-811e-00741b3da261",
    "c5bd1711-5a1a-4f87-bdb7-812f6d3a1ab8",
    "65570f0a-5a01-4911-bf08-0b15f19cc07d",
    "e9cac2d4-d628-4bad-8b81-621d70214bc2",
    "d3f4e905-b090-4225-9e0f-a5eb7fc72209",
    "fe028467-4d1f-45f1-b862-efa7f361ffa1",
    "a3922fe7-e120-4b73-867e-32f8ca56b671",
    "946a28cc-55a3-46d7-aa8b-c0f1e5279eb9",
    "fe66b352-141b-4223-9092-d307b2689dcb",
    "497d2fd1-9302-47e8-b434-16283d4b5534",
    "c54d5ba1-1e8f-4954-bed0-8297b89d1504",
    "81a3fa4e-9a1e-4e47-b17a-97cfd66ad652",
    "9f97252a-38fd-4ac8-a897-db70c1427ccc",
    "4c3de565-b5b4-4f7f-ad52-3b799892d588",
    "93e7285b-f932-48f1-8482-f8c17f90c54b",
    "378011bf-324c-458a-ad09-bb1dd20443a8",
    "3e83d3ed-25f0-49e4-85b3-17897fdbbc96",
    "782cccac-995a-4afd-b581-76582a6fd08d",
    "ec6e5c61-f66f-468a-b158-984442e0ffbd",
    "dc749bae-66f3-4308-949e-e058bbaab37d",
    "72c75cdc-d3e4-4ee4-a93d-8f62cf5e6416",
    "2b7ddbad-460a-48dd-b2cf-252018a53157",
    "db93d398-9c8e-4f1e-8fe4-f4dea5b8161a",
    "154973d6-8541-4a1a-a00b-4606e17af544",
    "d3a0368b-6cc6-4475-83ba-9fca46850287",
    "329dd969-1f1a-4a9a-a251-9134cc9e9959",
    "7f900348-bfce-4246-a34d-80b57807327a",
    "382382c1-ef3a-4a2b-9473-99b43e0ec3f3",
    "237b9cf9-2c2b-4bca-8abc-a0084bce31a5",
    "2b292521-efdc-4adb-a027-b4c83e7da2c5",
    "3b880b7a-8aad-4788-9136-8784136ec822",
    "82ed0b78-d76c-4e87-b590-7c400524768e",
    "daa4925b-80a0-44df-afe9-f65d34a73886",
    "71f28433-3f3c-4b70-a307-27dd54b8c0f4",
    "a4fa98b4-9161-4f80-883b-ac5f136b2f46",
    "9f11e510-7c8d-40a2-a726-22cef7e1fc43",
    "8aff63cb-900c-4ae3-83cf-f2db6da258bd",
    "0f483827-c7a9-4829-b0ed-b5c9ac9c10b8",
    "27e572af-83a9-46bf-80e0-4c871712b089",
    "c0c0d5ac-d6cb-471f-ba0b-3e960ed946a6",
    "1ecb1ea9-9ed6-49dd-bf8a-a70b2c182fb3",
    "4c0022bb-58c4-44f1-8f56-6074c062fdde",
    "32b16541-1e35-4e4c-a59a-2eb0de802dfe",
    "130f5334-2b7e-4eb3-9956-e6f6a3ea5e54",
    "a456d91b-883a-46c5-be94-a5750ec884c6",
    "1fba4b51-d7e4-44aa-a66e-92b9d8ce6b11",
    "f0ae57bf-26d8-4de4-8c1c-b041d3b7965f",
    "566b9e44-ed3a-4fbc-8099-95e3e4c94ce8",
    "7fa8255f-9db9-4c29-a615-8c20e8c9711e",
    "332ae292-c4bd-46fe-ae6c-2d696b6fbe48",
    "be41716f-cc56-406b-b2f8-4c0dcfbec950",
    "6e1b01d3-8c09-42f2-a6a7-9b8793359a19",
    "49e5d8b0-638a-4180-a9ec-47fa7a6a8a5c",
    "1b5ca186-ade1-4480-bfd4-d2dc30f77f2f"
    ] # Apex - Celebrity, Adventure of the seas - Royal Caribbean, Cloud - Silver Seas, Mein sheift 1 - TUI
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

def create_asset(type, site):
    uniq = random.randint(100000000, 999999999)
    code = f'{uniq} - {type['name']} - SCRIPT'

    url = "https://api.safetyculture.io/assets/v1/assets"

    payload = {
        "site": site,
        "code": code,
        "type_id": type['id']
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

def create_action(asset, group):
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
                    "group": { "group_id": group },
                    "collaborator_id": group
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
                    "group": { "group_id": group },
                    "collaborator_id": group
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

def link_template(action_id, template):
    url = f"https://api.safetyculture.io/tasks/v1/tasks/{action_id}/link_template"

    payload = {
        "template_ids": [
            template
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    } 
    response = requests.post(url, json=payload, headers=headers)
    return response

def create_schedule(asset, template, group):
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
            "id": template
        },
        "status": "ACTIVE",
        "description": title,
        "recurrence": f"FREQ=MONTHLY;BYDAY=MO;INTERVAL=1;DTSTART={dtstart}",
        "duration": "P1M",
        # "from_date": from_date,
        "assignees": [
            {
                "type": "ROLE",
                "id": group
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
        ret = id_val
    else:
        ret = response.json()
    return ret

def main():
    count = COUNT
    while count > 0:
        # site = rand_site()['site_uuid']
        site = rand_site()
        type = rand_type()
        if type['name'] == 'Emergency Escape Breathing Device (EEBD)': 
            template = '2665b4ec-7c7e-4867-b4c5-b2e24a540ccc'
        elif type['name'] == 'Fast Rescue Boat':
            template = '611098ae-5854-486e-900a-d2948ae6de5f'
        elif type['name'] == 'Lifeboat':
            template = 'c3ede204-8aa4-4d01-99e9-d9cd4cf64d7a'
        elif type['name'] == 'Marine Evacuation System':
            template = 'b822b93f-7bfe-4898-b661-967fb66ce4c5'
        else: # any fire extinguisher
            template = 'aa0e9746-7c50-40ce-b4a1-8d6c0f9c8fec'
        
        if site in [
            "939a9b6b-5a89-4f23-b493-ba3a902308cc",
            "ab78c250-a5d2-4f23-b70a-001aa001726a",
            "8ff891b1-8035-42e8-b498-59c74e5fbee1",
            "6f541713-aca3-4a27-839d-f676f2c03b48",
            "6bae9267-0f2f-4280-992c-7464838bad55",
            "6979db7d-2c84-41cd-bb8e-1f773ecf1d86",
            "c06a14a1-09f2-4e5a-9d50-d0e14d65010f",
            "539a62b6-facc-4be2-b716-9b361f8cd5cb",
            "b8e48ca6-d27d-424b-9052-abed6ec560d3",
            "ac131f60-54fe-4835-aaf4-669fe132f4b5",
            "e6574c3b-0034-43f3-81ae-d074e1537cbc",
            "4cadc3ae-d0db-4d11-b71a-a90119069b50",
            "8a2a2224-0fa3-49a0-8053-aa6d07427638",
            "0cab954e-5da5-4df6-9ff4-cdd32837236b",
            "697e2bbe-a14e-4089-aa27-1648f634345a",
            "8b3232b5-86a1-47ff-a5ed-e50de286bade",
            "4147923d-1683-444c-ada1-871e92687146",
            "ce277160-3044-4cf8-b9d3-d281d80d6bc5",
            "7d08870a-03a0-41d7-9ba5-3f7d41fb32e7",
            "eba985c9-b1c4-461a-b72e-ba14ebf0d14c",
            "f1786407-b488-4d2e-bc3f-3350cf76c6cd",
            "60aec4fd-f475-466b-a1e9-f87a386ea62f",
            "98b3ec43-abed-4d82-8436-8b35cd12e795"
            ]: # Apex (AX)
            group = 'e621b66a-102c-43e0-8add-d1e8b1b2b3d7'
        elif site in [
            "7ea9621c-9891-48b1-8fe9-bd396e7eba66",
            "788d4f29-c2a1-485a-909f-a26e560c6263",
            "c096c4a7-8099-422d-ac18-0c90908d05c3",
            "13b035dd-0578-4370-972a-ded835d53441",
            "325c8d50-26c9-416f-9a58-832c463ffeaf",
            "fa1ab1ac-ef4e-4ab9-bf26-f79016cbdd5d",
            "09d0d4b2-7b77-4174-b153-5fef5b050a06",
            "744cd2ba-0fd6-4437-97d6-cc3268c26b7b",
            "58ca7b0d-fcea-4411-8f2a-0009c6565318",
            "a0a4bc83-edf8-4bcb-bdc1-c56123363f36",
            "433793e8-bdcb-47d5-b2c9-15403285ac1a",
            "6603a219-5c3a-4bea-a77e-235f57b42f73",
            "def517a7-e19e-4224-a94d-ed264368c522",
            "3a1d981a-26b4-4168-9612-632350a866ce",
            "14b1a61c-c482-42f6-8ffa-ecaeae46072d",
            "7801998a-1971-4007-811e-00741b3da261",
            "c5bd1711-5a1a-4f87-bdb7-812f6d3a1ab8",
            "65570f0a-5a01-4911-bf08-0b15f19cc07d",
            "e9cac2d4-d628-4bad-8b81-621d70214bc2",
            "d3f4e905-b090-4225-9e0f-a5eb7fc72209",
            "fe028467-4d1f-45f1-b862-efa7f361ffa1",
            "a3922fe7-e120-4b73-867e-32f8ca56b671",
            "946a28cc-55a3-46d7-aa8b-c0f1e5279eb9"
            ]: # Adventure of the seas
            group = '6d415159-2f3c-43ad-91b3-32724149c25c'
        elif site in [
            "fe66b352-141b-4223-9092-d307b2689dcb",
            "497d2fd1-9302-47e8-b434-16283d4b5534",
            "c54d5ba1-1e8f-4954-bed0-8297b89d1504",
            "81a3fa4e-9a1e-4e47-b17a-97cfd66ad652",
            "9f97252a-38fd-4ac8-a897-db70c1427ccc",
            "4c3de565-b5b4-4f7f-ad52-3b799892d588",
            "93e7285b-f932-48f1-8482-f8c17f90c54b",
            "378011bf-324c-458a-ad09-bb1dd20443a8",
            "3e83d3ed-25f0-49e4-85b3-17897fdbbc96",
            "782cccac-995a-4afd-b581-76582a6fd08d",
            "ec6e5c61-f66f-468a-b158-984442e0ffbd",
            "dc749bae-66f3-4308-949e-e058bbaab37d",
            "72c75cdc-d3e4-4ee4-a93d-8f62cf5e6416",
            "2b7ddbad-460a-48dd-b2cf-252018a53157",
            "db93d398-9c8e-4f1e-8fe4-f4dea5b8161a",
            "154973d6-8541-4a1a-a00b-4606e17af544",
            "d3a0368b-6cc6-4475-83ba-9fca46850287",
            "329dd969-1f1a-4a9a-a251-9134cc9e9959",
            "7f900348-bfce-4246-a34d-80b57807327a",
            "382382c1-ef3a-4a2b-9473-99b43e0ec3f3",
            "237b9cf9-2c2b-4bca-8abc-a0084bce31a5",
            "2b292521-efdc-4adb-a027-b4c83e7da2c5",
            "3b880b7a-8aad-4788-9136-8784136ec822"
            ]: # Cloud
            group = 'f4865c51-4b9b-488c-be0b-a729862fe0a4'
        else: # Mein Shiff 1
            group = '46cb9e80-8835-4f40-8020-59e98cf73ada'

        if type['name'] != 'Training Document':
            asset = create_asset(type, site)

            # if random.randint(0,1) == 0: #if 0, then create an action. Otherwise, create a schedule
            if type['name'] in ['Emergency Escape Breathing Device (EEBD)','Fast Rescue Boat','Lifeboat','Marine Evacuation System']:
                schedule = create_schedule(asset, template, group)
                print(f"Schedule - {schedule}, {count-1} Remaining")
            else:
                action = create_action(asset, group)
                link_template(action, template)
                print(f"Action Item - {action}, {count-1} Remaining")
            count -= 1

main()
