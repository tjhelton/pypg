import requests

TOKEN = 'TOKEN'

def feed_actions():
    url = 'https://api.safetyculture.io/feed/actions'
    headers = {'authorization': f'Bearer {TOKEN}', 'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    data = response.json()['data']

    return print(data)

feed_actions()
