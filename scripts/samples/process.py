# import csv

# SAMPLE_DOC = 'Ontivity User Provisioning.csv'

# def main():
#     with open(SAMPLE_DOC, newline='') as file:
#         raw = csv.DictReader(file)
#         array = [{'title': row.get('positionTitle'), 'group': row.get('group')} for row in raw]
#     print(array[:5])
#     return

# main()

import json

def import_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def process():
    i_raw = import_json('details.json')['inspection']
    a_raw = import_json('asset.json')['asset']
    metadata = i_raw['metadata']
    template = i_raw['template']
    items = i_raw['items']
    fields = a_raw['fields']

    date = metadata['completed_time']
    div_name = a_raw.get('site', '').get('name', '') # i4.0_Line question (Asset Site)
    home_code = next((row['string_value'] for row in fields if row['name'] == 'Home Code'), None)
    line = a_raw['code'] #asset code
    shift = next((row['question_item']['responses'][0]['value'] for row in items if row['label'] == 'i4.0_Shift'), None)

    output = []
    for row in items:
        if any(keyword in row['label'] for keyword in ('Start-up', '5S', 'LPA')) and row['type'] == 'section':
            module = row['label'] # section label
            score = row['combined_item_score']['combined_score_percentage'] # section score
            output.append({
                'date': date,
                'division_name': div_name,
                'home_code': home_code,
                'line': line,
                'shift': shift,
                'module': module,
                'score': score
            })
    return {
        'output': output
    }

