import os
import requests
import pandas as pd

TOKEN = ''

def read_csv():
    df = pd.read_csv('input.csv')
    csv = df.to_dict('records')
    return csv

def get_public_link(issue_id, count):
    count += 1
    try:
        url = f"https://api.safetyculture.io/tasks/v1/shared_link/{issue_id}/web_report"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }
        response = requests.post(url, headers=headers).json()
        url = response['url']
        status = f"#{count} SUCCESS Fetching Public Link For Issue: {issue_id}"
        log_row = [{"issue_id": issue_id, "url": url, "status": status}]
        print(status)
        return log_row
    except requests.exceptions.RequestException as err:
        status = f"#{count} ERROR Fetching Public Link For Issue: {issue_id}, {err}"
        log_row = [{"issue_id": issue_id, "url": "N/A", "status": status}]
        print(status)
        return log_row

def main():
    count = 0
    data = read_csv()
    for row in data:
        issue_id = row['issue_id']
        response = get_public_link(issue_id, count)
        response_df = pd.DataFrame(response)
        response_df.to_csv("output.csv", mode='a', header=not os.path.exists("output.csv"), index=False)

main()
        