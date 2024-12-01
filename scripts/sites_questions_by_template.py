import csv
import requests

TOKEN = 'TOKEN_HERE'

OUTPUT = []

def feed_templates():
    url = 'https://api.safetyculture.io/feed/templates'
    headers = {'authorization': f'Bearer {TOKEN}', 'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    data = response.json()['data']
    next_page = response.json().get('metadata', {}).get('next_page')

    while next_page:
        url = f'https://api.safetyculture.io{next_page}'
        response = requests.get(url, headers=headers)
        data.extend(response.json()['data'])
        next_page = response.json().get('metadata', {}).get('next_page')

    ids = [row['id'] for row in data]

    return ids

def get_site_question(template_id):
    url = f'https://api.safetyculture.io/templates/v1/templates/{template_id}'
    headers = {
        "accept": "application/json",
        "authorization": f'Bearer {TOKEN}'
    }
    response = requests.get(url, headers=headers)
    template = response.json().get('template', {})
    items = template.get('items', [])
    t_id = template.get('id', 'Unknown ID')
    name = template.get('name', 'Unknown Name')

    site_question_exists = 'No'
    is_mandatory = None

    for item in items:
        if item.get('label') == 'Title Page':
            for child in item.get('children', []):
                if 'site' in child:
                    site_question_exists = 'Yes'
                    is_mandatory = child['site']['options'].get('is_mandatory', False)

    OUTPUT.append({
        'id': t_id,
        'name': name,
        'site question exists?': site_question_exists,
        'is_mandatory?': is_mandatory
    })

def write_to_csv(filename):
    headers = ['id', 'name', 'site question exists?', 'is_mandatory?']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(OUTPUT)

def process():
    temps = feed_templates()
    for row in temps:
        get_site_question(row)
    write_to_csv('output.csv')

process()
