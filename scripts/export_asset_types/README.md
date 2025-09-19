# SafetyCulture Asset Types Fetcher

This Python script fetches all asset types from SafetyCulture via API and exports them to a CSV file. It retrieves asset type information including ID, name, category, and creation timestamp. This guide is for beginners to Python who want to run the script.

## Prerequisites
- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org/downloads/) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.

## Setup Instructions

1. **Install Python**
   - Download and install Python 3 from [python.org](https://www.python.org/downloads/).
   - During installation, check the box to add Python to your PATH (this makes it easier to run Python from the command line).

2. **Install Required Libraries**
   - Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux).
   - Run the following command to install the required Python libraries:
     ```
     pip install requests
     ```
   - This installs `requests` (for making API calls).

3. **Add Your API Token**
   - Open the script file (`main.py`) in a text editor.
   - Find the line `TOKEN = ''` near the top.
   - Replace `''` with your SafetyCulture API token, like this:
     ```python
     TOKEN = 'your-api-token-here'
     ```
   - Save the script.

## Running the Script
1. Open a terminal and navigate to the folder containing `main.py`. For example:
   ```
   cd path/to/your/folder
   ```
   (Replace `path/to/your/folder` with the actual path.)

2. Run the script by typing:
   ```
   python main.py
   ```

3. The script will:
   - Fetch all asset types from the SafetyCulture API.
   - Handle pagination automatically to retrieve all available asset types.
   - Save the results to a timestamped CSV file (e.g., `asset_types_20241201_143022.csv`).

## Output
- After running, check for the generated CSV file in the same folder. The filename includes a timestamp to avoid overwriting previous exports.
- The CSV file contains the following columns:
  - `id`: Unique identifier of the asset type
  - `name`: Name of the asset type
  - `category`: Category code of the asset type
  - `category_name`: Human-readable category name
  - `created_at`: Timestamp when the asset type was created

## Troubleshooting
- **Error: "No module named requests"**
  - Ensure you ran `pip install requests`.
- **Error: "Please set your SafetyCulture API token"**
  - Make sure you've replaced the empty `TOKEN = ''` with your actual API token.
- **API Errors**
  - Check that your API token is correct and valid.
  - Ensure your account has permission to access asset types via the API.
- **Permission Issues**
  - If you get permission errors, try running the terminal as an administrator (Windows) or with `sudo` (macOS/Linux).

## Notes
- The script uses the SafetyCulture API endpoint for listing asset types (`https://api.safetyculture.io/assets/v1/types/list`).
- The script automatically handles pagination to fetch all asset types, retrieving up to 100 asset types per API call.
- Keep your API token secure and do not share it publicly.
- The output CSV file includes a timestamp in the filename to prevent overwriting previous exports.

For more help, consult the [SafetyCulture API documentation](https://developer.safetyculture.com/) or ask a colleague familiar with Python.