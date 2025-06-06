import os
import requests
import pandas as pd

TOKEN = ''

def read_csv():
    csv_df = pd.read_csv('input.csv')
    csv_df = csv_df.fillna('')
    csv = csv_df.to_dict('records')
    return csv

def create_site(name, parent, count):
    try:
        url = "https://api.safetyculture.io/directory/v1/folder"
        if parent == '':
            payload = {
                "meta_label": "location",
                "name": name
            }
        else:
            payload = {
                "meta_label": "location",
                "parent_id": parent,
                "name": name
            }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        status = f"#{count} - Successfully Created {name}"
        print(status)
        return status
    except requests.exceptions.RequestException as error:
        status = f"#{count} - ERROR creating {name}: {error}"
        print(status)
        return status

def main():
    csv_data = read_csv()
    count = 0
    output_file = 'output.csv'

    for row in csv_data:
        name = row['name']
        parent = row.get('parent', None)
        old_id = row['site_id']
        status = create_site(name, parent, count)
        df = pd.DataFrame({
            'count': [count],
            'SiteName': [name],
            'Status': [status],
            'old_id': [old_id]
        })
        df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
        count += 1

main()
