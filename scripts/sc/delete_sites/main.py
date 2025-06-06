import os
import requests
import pandas as pd

TOKEN = ''

def read_csv():
    csv_df = pd.read_csv('input.csv')
    csv = csv_df.to_dict('records')
    return csv

def delete_site(site_id, count):
    try:
        url = f"https://api.safetyculture.io/directory/v1/folders?folder_ids={site_id}&cascade_up=true"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }
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
    csv_data = read_csv()
    count = 0
    output_file = 'output.csv'

    for row in csv_data:
        site_id = row['siteId']
        status = delete_site(site_id, count)
        df = pd.DataFrame({
            'count': [count],
            'SiteID': [site_id],
            'Status': [status]
        })
        df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
        count += 1

main()
