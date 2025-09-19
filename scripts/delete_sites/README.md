# SafetyCulture Site Deleter

This Python script deletes SafetyCulture sites (folders) in bulk using the SafetyCulture API. It reads site IDs from a CSV file, deletes each site via API calls, and logs the results to an output CSV file. This guide is for beginners to Python who want to run the script.

## Prerequisites
- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org/downloads/) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.
- **Input CSV File**: Create a CSV file named `input.csv` with site IDs you want to delete.

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
   - Create a file named `input.csv` in the same folder as the script.
   - The CSV should have a `siteId` column with site IDs to delete. For example:
     ```
     siteId
     f47ac10b-58cc-4372-a567-0e02b2c3d479
     f47ac10b-58cc-4372-a567-0e02b2c3d480
     ```
   - Save the file as `input.csv`. You can create it in a text editor or a spreadsheet program like Excel.

4. **Add Your API Token**
   - Open the script file (e.g., `main.py`) in a text editor.
   - Find the line `TOKEN = ''` near the top.
   - Replace `''` with your SafetyCulture API token, like this:
     ```python
     TOKEN = 'your-api-token-here'
     ```
   - Save the script.

## Running the Script
1. Open a terminal and navigate to the folder containing `main.py` and `input.csv`. For example:
   ```
   cd path/to/your/folder
   ```
   (Replace `path/to/your/folder` with the actual path.)

2. Run the script by typing:
   ```
   python main.py
   ```

3. The script will:
   - Read site IDs from `input.csv`.
   - Delete each site via SafetyCulture API calls with cascade option.
   - Display progress messages in the terminal.
   - Save the results to a file named `output.csv`.

## Output
- After running, check the `output.csv` file in the same folder. It will contain:
  - A column for the `count` (processing order).
  - A column for the `SiteID` that was processed.
  - A column for the `Status` showing success or error messages.

## Troubleshooting
- **Error: "No module named pandas" or "No module named requests"**
  - Ensure you ran `pip install pandas requests`.
- **Error: "File input.csv not found"**
  - Make sure `input.csv` is in the same folder as the script and is correctly formatted.
- **API Errors**
  - Check that your API token is correct and valid.
  - Ensure you have permissions to delete sites in SafetyCulture.
  - Verify that the site IDs exist and are correct.
- **Permission Issues**
  - If you get permission errors, try running the terminal as an administrator (Windows) or with `sudo` (macOS/Linux).

## Important Warnings
- **This action is irreversible** - deleted sites cannot be easily restored.
- The script uses `cascade_up=true` which may delete parent folders if they become empty.
- Always verify your site IDs before running the script.
- Test with a small subset first to ensure everything works as expected.

## Notes
- The script deletes sites sequentially and logs all results.
- Keep your API token secure and do not share it publicly.
- Make sure you have proper authorization to delete the specified sites.

For more help, consult the [SafetyCulture API documentation](https://developer.safetyculture.com/reference/directoryservice_deletefolders) or ask a colleague familiar with Python.