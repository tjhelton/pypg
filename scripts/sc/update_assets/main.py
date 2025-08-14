import time
import requests
import pandas as pd
import os

TOKEN = ""  

def read_csv():
    csv_df = pd.read_csv("assets.csv").fillna("")
    csv_array = csv_df.to_dict("records")
    return csv_array

def log_results(results_array):
    for row in results_array:
        asset_id = row["asset_id"]  
        code = row["code"]
        status = row["status"]
        message = row["message"]
        df = pd.DataFrame(
            {"asset_id": [asset_id], "code": [code], "status": [status], "message": [message]}
        )
        df.to_csv(
            "output.csv", mode="a", header=not os.path.exists("output.csv"), index=False
        )

def map_csv(csv):
    assets = []
    for row in csv:
        asset = {
            "asset_id": row['Internal ID'],  
            "code": row.get('Unique ID', ''),
            "fields": [
                {
                    "field_id": "ef1223ac-dfb5-11ec-9d64-0242ac120003",
                    "string_value": f"{row['Display name']}",
                },
                {
                    "field_id": "ae72d2e0-ee57-4a6e-bbd0-4bb56f768cff",
                    "string_value": f"{row['Location']}",
                },
                {
                    "field_id": "5550e2f4-f3cb-4131-a69b-aa3df095588c",
                    "string_value": f"{row['Zone']}",
                },
                {
                    "field_id": "34e91098-a802-4d56-b6b6-ff9d34e0b6de",
                    "string_value": f"{row['Side']}",
                },
                {
                    "field_id": "bacba43f-9355-46bd-b96f-a555672feae6",
                    "string_value": f"{row['Notes']}",
                },
                {
                    "field_id": "6ecd7bcc-6eea-40b4-a1b0-e8174b07cabd",
                    "string_value": f"{row['Subtype']}",
                },
            ]
        }
        assets.append(asset)
    return assets

def update_asset(asset):
    asset_id = asset["asset_id"]  
    fields = asset["fields"]
    code = asset["code"]
    url = f"https://api.safetyculture.io/assets/v1/assets/{asset_id}/fields"
    payload = {"fields": fields}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {TOKEN}",
    }
    max_retries = 3
    delay = 5
    for attempt in range(max_retries):
        try:
            response = requests.patch(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Successfully updated asset {asset_id}. Response: {response.status_code}")
            return {"asset_id": asset_id, "code": code, "status": "SUCCESS", "message": "SUCCESS"}
        except requests.exceptions.RequestException as e:
            print(f"Error updating asset {asset_id}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                print("Max retries reached. Giving up.")
                return {"asset_id": asset_id, "code": code, "status": "ERROR", "message": str(e)}

def main():
    assets = read_csv()
    mapped_assets = map_csv(assets)
    total_assets = len(mapped_assets)
    print(f"Total assets to process: {total_assets}")
    for asset in mapped_assets:
        result = update_asset(asset)
        log_results([result])

    main()
    