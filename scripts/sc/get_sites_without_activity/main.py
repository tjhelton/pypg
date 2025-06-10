import os
import requests
import pandas as pd

TOKEN = ''

def write_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', header=not os.path.exists(filename), index=False)

def feed_sites():
    relative_url = '/feed/sites?include_deleted=false&show_only_leaf_nodes=true'
    sites = []
    count = 0
    while relative_url:
        try:
            url = f"https://api.safetyculture.io{relative_url}"
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {TOKEN}"
            }
            response = requests.get(url, headers=headers).json()
            data = response['data']
            sites.extend(data)
            count += 1
            remaining = response['metadata'].get('remaining_records','0')
            print(f"Fetching Sites - Page {count} - {remaining} Remaining")
            relative_url = response['metadata'].get('next_page', None)
            if relative_url is None:
                print("All Sites Retrieved")
        except requests.exceptions.RequestException as err:
            print(f"ERROR: {err}")
    return sites

def feed_inspections():
    relative_url = "/feed/inspections?archived=false&completed=both"
    inspections = []
    count = 0
    while relative_url:
        try:
            url = f"https://api.safetyculture.io{relative_url}"
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {TOKEN}"
            }
            response = requests.get(url, headers=headers).json(),
            data = response['data']
            inspections.extend(data)
            count += 1
            total = len(inspections)
            remaining = response['metadata'].get('remaining_records','0')
            print(f"Fetching Inspections - Page {count} - {total} Fetched Total - {remaining} Remaining")
            relative_url = response['metadata'].get('next_page', None)
            if relative_url is None:
                print("All Inspections Retrieved")
        except requests.exceptions.RequestException as err:
            print(f"ERROR: {err}")
    return inspections

def delete_site(site_id):
    try:
        url = f"https://api.safetyculture.io/directory/v1/folders?folder_ids={site_id}&cascade_up=true&domain=location"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }
        requests.delete(url, headers=headers)
        status = 'SUCCESS'
        print(f"Success Deleting Site - {site_id}")
        return status
    except requests.exceptions.RequestException as err:
        print(f"ERROR Deleting Site - {err}")
        return err

def get_inspection(audit_id):
    try:
        url = f"https://api.safetyculture.io/inspections/v1/inspections/{audit_id}/details"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }
        response = requests.get(url, headers=headers).json()
        site_id = response['inspection']['metadata'].get('site', None).get('site_id', None)
        print(site_id)
    except requests.exceptions.RequestException as err:
        print(f"ERROR Fetching Inspection {audit_id} - {err}")
    return site_id

def get_site_status(site_id):
    try:
        url = f"https://api.safetyculture.io/directory/v1/folder/{site_id}"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }
        response = requests.get(url, headers=headers).json()
        deleted = response['deleted']
        if deleted is True:
            status = "deleted"
        else:
            status = "active"
    except requests.exceptions.RequestException as err:
        print(f"ERROR Fetching Site {site_id} - {err}")
    return status

def find_inactive_sites(sites, inspections):
    no_activity = []
    sites_with_activity = {row['site_id'] for row in inspections}

    for row in sites:
        site_id = row['id']
        if site_id not in sites_with_activity:
            no_activity.append(row)
    print(f"{len(no_activity)}/{len(sites)} Sites Have No Inspection Activity")
    return no_activity

def main():
    sites = feed_sites()
    write_csv(sites, "sites.csv")
    inspections = feed_inspections()
    write_csv(inspections, "inspections.csv")
    no_activity = find_inactive_sites(sites, inspections)
    write_csv(no_activity, "no_inspection_activity.csv")

main()
