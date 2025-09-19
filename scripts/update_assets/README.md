# SafetyCulture Asset Updater

This Python script updates SafetyCulture asset field values in bulk using the SafetyCulture API. It reads asset information from a CSV file, maps the data to specific asset fields, and updates each asset via API calls with retry logic. This guide is for beginners to Python who want to run the script.

## Prerequisites
- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org/downloads/) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.
- **Input CSV File**: Create a CSV file named `assets.csv` with asset data to update.

## Setup Instructions

1. **Install Python**
   - Download and install Python 3 from [python.org](https://www.python.org/downloads/).
   - During installation, check the box to add Python to your PATH (this makes it easier to run Python from the command line).

2. **Install Required Libraries**
   - Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux).
   - Run the following command to install the required Python libraries:
     ```
     pip install pandas requests
     ```
   - This installs `pandas` (for handling CSV files) and `requests` (for making API calls).

3. **Prepare the Input CSV File**
   - Create a file named `assets.csv` in the same folder as the script.
   - The CSV should have the following required columns:
     ```
     Internal ID,Unique ID,Display name,Location,Zone,Side,Notes,Subtype
     asset-123,ASSET-001,Main Pump,Building A,Zone 1,North,Regular maintenance required,Centrifugal Pump
     asset-456,ASSET-002,Backup Generator,Building B,Zone 2,South,Emergency power supply,Diesel Generator
     ```
   - Save the file as `assets.csv`. You can create it in a text editor or a spreadsheet program like Excel.

4. **Add Your API Token**
   - Open the script file (e.g., `main.py`) in a text editor.
   - Find the line `TOKEN = ""` near the top.
   - Replace `""` with your SafetyCulture API token, like this:
     ```python
     TOKEN = "your-api-token-here"
     ```
   - Save the script.

## Running the Script
1. Open a terminal and navigate to the folder containing `main.py` and `assets.csv`. For example:
   ```
   cd path/to/your/folder
   ```
   (Replace `path/to/your/folder` with the actual path.)

2. Run the script by typing:
   ```
   python main.py
   ```

3. The script will:
   - Read asset data from `assets.csv`.
   - Map the CSV data to SafetyCulture asset field IDs.
   - Update each asset via SafetyCulture API calls with automatic retry on failures.
   - Display progress messages in the terminal.
   - Save the results to a file named `output.csv`.

## Field Mapping
The script maps CSV columns to specific SafetyCulture asset field IDs:
- **Display name** → Display Name field
- **Location** → Location field
- **Zone** → Zone field
- **Side** → Side field
- **Notes** → Notes field
- **Subtype** → Subtype field

*Note: The field IDs in the script are pre-configured. You may need to update them to match your organization's asset template.*

## Output
- After running, check the `output.csv` file in the same folder. It will contain:
  - A column for the `asset_id` that was processed.
  - A column for the `code` (Unique ID from input).
  - A column for the `status` showing "SUCCESS" or "ERROR".
  - A column for the `message` with details about the result.

## Troubleshooting
- **Error: "No module named pandas" or "No module named requests"**
  - Ensure you ran `pip install pandas requests`.
- **Error: "File assets.csv not found"**
  - Make sure `assets.csv` is in the same folder as the script and is correctly formatted.
- **API Errors**
  - Check that your API token is correct and valid.
  - Ensure you have permissions to update assets.
  - Verify that the asset IDs in the "Internal ID" column exist and are correct.
- **Field ID Errors**
  - The script uses hardcoded field IDs that may not match your organization's asset template.
  - Contact your SafetyCulture administrator to get the correct field IDs for your asset template.
- **Permission Issues**
  - If you get permission errors, try running the terminal as an administrator (Windows) or with `sudo` (macOS/Linux).

## Retry Logic
The script includes automatic retry functionality:
- **3 retry attempts** for each failed update
- **Exponential backoff** (5, 10, 20 seconds between retries)
- **Automatic failure handling** if all retries are exhausted

## Use Cases
- **Asset Data Migration**: Transfer asset information from external systems
- **Bulk Asset Updates**: Update multiple asset fields across many assets
- **Data Synchronization**: Keep asset information synchronized with other databases
- **Template Deployment**: Populate asset fields when implementing new asset templates
- **Data Cleanup**: Standardize and clean up existing asset information

## Important Notes
- The script processes assets sequentially with built-in retry logic for reliability.
- Keep your API token secure and do not share it publicly.
- Test with a small `assets.csv` first to ensure field mappings are correct.
- The "Internal ID" column must contain valid SafetyCulture asset IDs.
- Field IDs in the script may need to be updated to match your organization's asset template.

For more help, consult the [SafetyCulture API documentation](https://developer.safetyculture.com/reference/assetsservice_updateassetfields) or ask a colleague familiar with Python.