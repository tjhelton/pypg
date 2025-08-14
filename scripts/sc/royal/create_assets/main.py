import os
import time
import requests
import pandas as pd

TOKEN = ""
SHIP_CODE = 'SHIP_CODE_HERE_DO_NOT_FORGET_TO_SET'

def read_csv():
    csv_df = pd.read_csv("assets.csv").fillna("")
    csv_array = csv_df.to_dict("records")
    return csv_array

def random_id():
    return random.randint(1000000, 9999999)

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
        identifier = random_id()
        code = f"{SHIP_CODE}-{row['Deck']}-{row['MFZ']}-{row['ShipSide']}-{identifier}"
        asset = {
            "code": code,
            "type_id": row["type_id"],
            "site_id": row["site_id"],
            "fields": [
                {
                    "field_id": "ef1223ac-dfb5-11ec-9d64-0242ac120003",
                    "string_value": f"{row['DisplayName']}",
                },
                {
                    "field_id": "ae72d2e0-ee57-4a6e-bbd0-4bb56f768cff",
                    "string_value": f"{row['Location']}",
                },
                {
                    "field_id": "5550e2f4-f3cb-4131-a69b-aa3df095588c",
                    "string_value": f"{row['MFZ']}",
                },
                {
                    "field_id": "34e91098-a802-4d56-b6b6-ff9d34e0b6de",
                    "string_value": f"{row['ShipSide']}",
                },
                {
                    "field_id": "bacba43f-9355-46bd-b96f-a555672feae6",
                    "string_value": f"{row['Notes']}",
                },
                {
                    "field_id": "6ecd7bcc-6eea-40b4-a1b0-e8174b07cabd",
                    "string_value": f"{row['subtype']}",
                },
            ],
        }
        assets.append(asset)
    return assets

def chunk_assets(assets):
    for i in range(0, len(assets), 300):
        yield assets[i:i + 300]

def create_assets(chunk):
    max_retries = 3
    delay = 5
    for attempt in range(max_retries):
        try:
            url = "https://api.safetyculture.io/assets/v1/assets/bulk"
            payload = {"assets": chunk}
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {TOKEN}",
            }
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            created = response.json().get("created_assets", [])
            failed = response.json().get("failed_assets", [])
            print(
                f"Successfully sent chunk of {len(created)} assets. Response: {response.status_code}"
            )
            return created, failed
        except requests.exceptions.RequestException as e:
            print(f"Error sending chunk: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                print("Max retries reached. Giving up.")
                return [], []

def main():
    assets = read_csv()
    mapped_assets = map_csv(assets)
    total_assets = len(assets)
    print(f"Total assets to process: {total_assets}")
    chunks = list(chunk_assets(mapped_assets))
    print(f"Split into {len(chunks)} chunks of up to 300 assets each.")
    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i}/{len(chunks)}...")
        created, failed = create_assets(chunk)
        created_results = [
            {
                "asset_id": row["id"],
                "code": row["code"],
                "status": "SUCCESS",
                "message": "SUCCESS",
            }
            for row in created
        ]
        failed_results = [
            {
                "asset_id": "ERROR",
                "code": row["code"],
                "status": "ERROR",
                "message": str(row)
            }
            for row in failed
        ]
        log_results(created_results)
        log_results(failed_results)

main()
