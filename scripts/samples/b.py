import json

def import_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def process():
    fields = import_json('asset.json')['asset']['fields']
    home_code = [row['string_value'] for row in fields][0]
    print(home_code)
process()

# home code, plant, area, line, display name
