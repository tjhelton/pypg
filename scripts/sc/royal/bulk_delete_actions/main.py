import requests
import pandas as pd

TOKEN = ''

def read_csv():
    df = pd.read_csv('input.csv')
    csv = df.to_dict('records')
    return csv

def chunk_actions(actions):
    for i in range(0, len(actions), 300):
        yield actions[i:i + 300]

def delete_actions(actions):
    url = "https://api.safetyculture.io/tasks/v1/actions/delete"
    payload = {"ids": actions}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

def main():
    csv = read_csv()
    actions = [row['id'] for row in csv]
    chunked = list(chunk_actions(actions))
    for chunk in chunked:
        delete_actions(chunk)

    main()
    