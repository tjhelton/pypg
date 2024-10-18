import csv
import requests

TOKEN = 'TOKEN'

def list_sensors():
    url = 'https://api.safetyculture.io/sensors/v1/sensors/list'
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }
    response = requests.post(url, headers=headers).json()['sensors']
    clean = [{'source_name': row['source_name'], 'source_id': row['source_id'], 'asset': row['asset_name'], 'location': row['location_name']} for row in response]
    return clean

def main(input):
    output = []
    for row in input:
        asset = row['asset']
        location = row['location']
        source = row['source_name']
        id = row['source_id']
        url = f'https://api.safetyculture.io/sensors/v1/sensors/{source}/{id}/latest-readings'
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {TOKEN}"
        }
        response = requests.get(url, headers=headers).json()['readings']
        for row in response:
            if row['type'] == 'Temperature' or row['type'] == 'Humidity':
                output.append({
                    'type': row['type'],
                    'value': row['value'],
                    'measurement': row['unit'],
                    'asset': asset,
                    'location': location
                })
    return print(output)

main(list_sensors())
