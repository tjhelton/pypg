import json
import requests
import csv

TOKEN = 'TOKEN'

def feed_logs():
    url = 'https://api.safetyculture.io/feed/activity_log_events'
    headers = {'accept': 'application/json', 'authorization': f'Bearer {TOKEN}'}
    response = requests.get(url, headers=headers).json()
    data = response.get('data', [])
    next_page = response.get('metadata', {}).get('next_page', '')

    while next_page:
        response = requests.get(f'https://api.safetyculture.io{next_page}', headers=headers).json()
        data_to_add = response.get('data', [])
        data.extend(data_to_add)
        next_page = response.get('metadata', {}).get('next_page', '')

    cloned_a = [{
        'original': json.loads(row.get('metadata')).get('cloned_from_inspection_id'),
        'copy': json.loads(row.get('metadata', '')).get('inspection_id'),
        'user': row.get('user_id', '')
    } for row in data if row['type'] == 'inspection.cloned']

    return cloned_a

def enrich_inspection(cloned_a):
    cloned_b = []
    for row in cloned_a:
        sid = row.get('copy', '')
        url = f'https://api.safetyculture.io/inspections/v1/inspections/{sid}/details'
        headers = {'accept': 'application/json', 'authorization': f'Bearer {TOKEN}'}
        response = requests.get(url, headers=headers).json()
        template = response.get('inspection').get('template').get('template_name')
        site = response.get('inspection').get('metadata').get('site').get('site_name')
        modified = response.get('inspection').get('metadata').get('last_modified_time')
        cloned_b.append({
            'original': row.get('original', ''),
            'copy': row.get('copy', ''),
            'user': row.get('user', ''),
            'template': template,
            'site': site,
            'lm': modified
        })
    return cloned_b

def enrich_user(cloned_b):
    cloned_c = []
    for row in cloned_b:
        uid = row.get('user', '')
        url = f'https://api.safetyculture.io/users/{uid}'
        headers = {'accept': 'application/json', 'authorization': f'Bearer {TOKEN}'}
        response = requests.get(url, headers=headers).json()
        first = response.get('firstname', '')
        last = response.get('lastname', '')
        full = f'{first} {last}'
        orig = 'audit_'+row.get('original', '').replace('-','')
        cop = 'audit_'+row.get('copy', '').replace('-','')
        cloned_c.append({
            'original_id': orig,
            'copy_id': cop,
            'user': full,
            'template': row.get('template', ''),
            'site': row.get('site', ''),
            'copy_last_modified': row.get('lm', ''),
            'original_link': f'https://app.safetyculture.com/inspection/{orig}',
            'copy_link': f'https://app.safetyculture.com/inspection/{cop}',
        })
    return cloned_c

def write_csv():
    a = feed_logs()
    b = enrich_inspection(a)
    c = enrich_user(b)
    fieldnames = c[0].keys()
    with open('duplicated_inspections.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(c)

write_csv()
