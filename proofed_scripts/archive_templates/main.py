import pandas as pd
import requests

TOKEN = ''  # Add your API token here

def import_csv():
    df = pd.read_csv('input.csv').fillna('')
    csv = df.to_dict('records')
    return csv

def archive_template(template_id):
    url = f"https://api.safetyculture.io/templates/v1/templates/{template_id}/archive"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }
    response = requests.post(url, headers=headers)
    return response.text

def main():
    output = []
    templates = import_csv()
    for row in templates:
        template_id = row.get('template_id', row)  # Support both dict and string formats
        result = archive_template(template_id)
        output.append({"template_id": template_id, "result": result})
    output_df = pd.DataFrame(output)
    output_df.to_csv('log_output.csv', index=False)

main()
