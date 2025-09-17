import os
import time
import requests
import pandas as pd

TOKEN = ""

def map_csv_row(row):
    return {
        "asset_id": row['Internal ID'],
        "code": row.get('Unique ID', ''),
        "fields": [
            {"field_id": "ef1223ac-dfb5-11ec-9d64-0242ac120003", "string_value": str(row['Display name'])},
            {"field_id": "ae72d2e0-ee57-4a6e-bbd0-4bb56f768cff", "string_value": str(row['Location'])},
            {"field_id": "5550e2f4-f3cb-4131-a69b-aa3df095588c", "string_value": str(row['Zone'])},
            {"field_id": "34e91098-a802-4d56-b6b6-ff9d34e0b6de", "string_value": str(row['Side'])},
            {"field_id": "bacba43f-9355-46bd-b96f-a555672feae6", "string_value": str(row['Notes'])},
            {"field_id": "6ecd7bcc-6eea-40b4-a1b0-e8174b07cabd", "string_value": str(row['Subtype'])},
        ]
    }

def update_asset(asset):
    asset_id, code = asset["asset_id"], asset["code"]
    url = f"https://api.safetyculture.io/assets/v1/assets/{asset_id}/fields"
    headers = {"authorization": f"Bearer {TOKEN}"}
    for attempt in range(3):
        try:
            response = requests.patch(url, json={"fields": asset["fields"]}, headers=headers)
            response.raise_for_status()
            print(f"Successfully updated asset {asset_id}. Response: {response.status_code}")
            return {"asset_id": asset_id, "code": code, "status": "SUCCESS", "message": "SUCCESS"}
        except requests.exceptions.RequestException as e:
            print(f"Error updating asset {asset_id}: {e}")
            if attempt < 2:
                delay = 5 * (2 ** attempt)
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Giving up.")
                return {"asset_id": asset_id, "code": code, "status": "ERROR", "message": str(e)}

def main():
    csv_data = pd.read_csv("assets.csv").fillna("").to_dict("records")
    mapped_assets = [map_csv_row(row) for row in csv_data]
    print(f"Total assets to process: {len(mapped_assets)}")
    for asset in mapped_assets:
        result = update_asset(asset)
        pd.DataFrame([result]).to_csv("output.csv", mode="a", header=not os.path.exists("output.csv"), index=False)

main()
