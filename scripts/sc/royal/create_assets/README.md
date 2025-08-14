# SafetyCulture Bulk Asset Creator

This Python script creates assets in bulk in SafetyCulture via API. It reads asset details from a CSV file (`assets.csv`), generates unique asset codes, sends creation requests to the SafetyCulture API, and logs the results to an output CSV file (`output.csv`). The script includes retry logic for handling API errors and processes assets in chunks to manage API limits. This guide is for beginners to Python who want to run the script.

## Prerequisites

- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.
- **Ship Code**: Replace `SHIP_CODE_HERE_DO_NOT_FORGET_TO_SET` in the script with your ship code.
- **Input CSV File**: Create a CSV file named `assets.csv` with columns for asset details.

## Setup Instructions

### Install Python

1. Download and install Python 3 from [python.org](https://www.python.org).
2. During installation, check the box to add Python to your PATH (this makes it easier to run Python from the command line).

### Install Required Libraries

1. Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux).
2. Run the following command to install the required Python libraries:
   ```bash
   pip install pandas requests
   ```
   This installs `pandas` (for handling CSV files) and `requests` (for making API calls).

### Prepare the Input CSV File

1. Create a file named `assets.csv` in the same folder as the script.
2. The CSV should have the following columns:
   - `Deck`: The deck identifier for the asset.
   - `MFZ`: The multi-functional zone identifier.
   - `ShipSide`: The ship side (e.g., port or starboard).
   - `DisplayName`: The display name of the asset.
   - `Location`: The location of the asset.
   - `Notes`: Additional notes about the asset.
   - `subtype`: The subtype of the asset.
   - `type_id`: The asset type ID.
   - `site_id`: The site ID where the asset will be created.

3. Example `assets.csv`:
   ```csv
   Deck,MFZ,ShipSide,DisplayName,Location,Notes,subtype,type_id,site_id
   "Main Deck","Zone1","Port","Engine A","Engine Room","Check weekly","Engine","type_123456","site_789012"
   "Upper Deck","Zone2","Starboard","Pump B","Pump Area","Inspect daily","Pump","type_234567","site_789012"
   ```

4. Save the file as `assets.csv`. You can create it in a text editor or a spreadsheet program like Excel.

### Add Your API Token and Ship Code

1. Open the script file (e.g., `main.py`) in a text editor.
2. Find the line `TOKEN = ''` near the top.
3. Replace `''` with your SafetyCulture API token, like this:
   ```python
   TOKEN = 'your-api-token-here'
   ```
4. Find the line `SHIP_CODE = 'SHIP_CODE_HERE_DO_NOT_FORGET_TO_SET'`.
5. Replace `'SHIP_CODE_HERE_DO_NOT_FORGET_TO_SET'` with your ship code, like this:
   ```python
   SHIP_CODE = 'your-ship-code-here'
   ```
6. Save the script.

## Running the Script

1. Open a terminal and navigate to the folder containing `main.py` and `assets.csv`. For example:
   ```bash
   cd path/to/your/folder
   ```
   (Replace `path/to/your/folder` with the actual path.)

2. Run the script by typing:
   ```bash
   python main.py
   ```

The script will:
- Read asset details from `assets.csv`.
- Generate a unique asset code for each asset using the format `SHIP_CODE-Deck-MFZ-ShipSide-randomID`.
- Split assets into chunks of up to 300 for API processing.
- Send asset creation requests to the SafetyCulture API for each chunk.
- Log the results to `output.csv`.
- Print progress and API response statuses to the console.

## Output

After running, check the `output.csv` file in the same folder. It will contain:
- `asset_id`: The ID of the created asset (or "ERROR" if creation failed).
- `code`: The generated asset code.
- `status`: Either `SUCCESS` or `ERROR` based on the API response.
- `message`: Additional details, such as error messages if the asset creation failed.

The console will display progress (e.g., "Processing chunk 1/2...") and API response statuses (e.g., "Successfully sent chunk of 300 assets. Response: 200").

## Troubleshooting

### Error: "No module named pandas" or "No module named requests"
- Ensure you ran `pip install pandas requests`.

### Error: "File assets.csv not found"
- Make sure `assets.csv` is in the same folder as the script and is correctly formatted.

### API Errors
- Check that your API token is correct and valid.
- Ensure all required fields in `assets.csv` (e.g., `Deck`, `MFZ`, `ShipSide`, `type_id`, `site_id`) are correct and correspond to existing entities in SafetyCulture.
- Verify that UUIDs (e.g., `type_id`, `site_id`) are valid and exist in SafetyCulture.

### Permission Issues
- If you get permission errors, try running the terminal as an administrator (Windows) or with `sudo` (macOS/Linux).

### Retry Failures
- The script retries failed API requests up to 3 times with increasing delays. If all retries fail, check the API endpoint and payload in the console output for debugging.

## Notes

- The script uses the SafetyCulture API endpoint for creating assets in bulk (`https://api.safetyculture.io/assets/v1/assets/bulk`). Verify the API documentation if you encounter issues.
- Keep your API token secure and do not share it publicly.
- Test with a small `assets.csv` file first to ensure everything works, especially if creating many assets.
- The script processes assets in chunks of 300 to respect API limits.
- The script includes retry logic (3 attempts with exponential backoff) to handle temporary API issues.
- Ensure all UUIDs (e.g., `type_id`, `site_id`, and field IDs) are valid and exist in SafetyCulture.

For more help, consult the SafetyCulture API documentation or ask a colleague familiar with Python.