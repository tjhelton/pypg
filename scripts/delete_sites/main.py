import os
import requests
import pandas as pd

TOKEN = ''

def delete_site(site_id, count):
    try:
        url = f"https://api.safetyculture.io/directory/v1/folders?folder_ids={site_id}&cascade_up=true"
        headers = {"authorization": f"Bearer {TOKEN}"}
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        status = f"{count} - {site_id} Deleted"
        print(status)
        return status
    except requests.exceptions.RequestException as error:
        status = f"#{count} - Error deleting {site_id}: {error}"
        print(status)
        return status

def main():
    csv_data = pd.read_csv('input.csv').to_dict('records')
    output_file = 'output.csv'
    for count, row in enumerate(csv_data):
        site_id = row['siteId']
        status = delete_site(site_id, count)
        pd.DataFrame({'count': [count], 'SiteID': [site_id], 'Status': [status]}).to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)

main()
