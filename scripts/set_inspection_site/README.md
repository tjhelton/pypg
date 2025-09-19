# SafetyCulture Inspection Site Assignment

This Python script assigns sites (locations) to existing SafetyCulture inspections in bulk using the SafetyCulture API. It reads audit IDs and site IDs from a CSV file, assigns each site to the corresponding inspection, and logs the results to an output CSV file. This guide is for beginners to Python who want to run the script.

## Prerequisites
- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org/downloads/) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.
- **Input CSV File**: Create a CSV file named `input.csv` with audit IDs and corresponding site IDs.

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
   - The CSV should have `audit_id` and `site_id` columns. For example:
     ```
     audit_id,site_id
     audit_f47ac10b58cc4372a5670e02b2c3d479,f47ac10b-58cc-4372-a567-0e02b2c3d480
     audit_f47ac10b58cc4372a5670e02b2c3d481,f47ac10b-58cc-4372-a567-0e02b2c3d482
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
   - Read audit IDs and site IDs from `input.csv`.
   - Assign each site to the corresponding inspection via SafetyCulture API calls.
   - Display progress messages in the terminal.
   - Save the results to a file named `output.csv`.

## Output
- After running, check the `output.csv` file in the same folder. It will contain:
  - A column for the `audit_id` that was processed.
  - A column for the `site_id` that was assigned.
  - A column for the `status` showing success or error messages.

## Troubleshooting
- **Error: "No module named pandas" or "No module named requests"**
  - Ensure you ran `pip install pandas requests`.
- **Error: "File input.csv not found"**
  - Make sure `input.csv` is in the same folder as the script and is correctly formatted.
- **API Errors**
  - Check that your API token is correct and valid.
  - Ensure you have permissions to modify inspections and access sites.
  - Verify that both audit IDs and site IDs exist and are correct.
- **Permission Issues**
  - If you get permission errors, try running the terminal as an administrator (Windows) or with `sudo` (macOS/Linux).

## Use Cases
- **Bulk Site Assignment**: Assign sites to multiple inspections at once
- **Data Migration**: Transfer site assignments from one system to another
- **Compliance Setup**: Ensure inspections are properly associated with their locations
- **Organizational Restructuring**: Update site assignments after location changes
- **Template Implementation**: Assign sites when rolling out new inspection templates

## Important Notes
- The script assigns sites to existing inspections - both audit IDs and site IDs must already exist.
- Keep your API token secure and do not share it publicly.
- If assigning many site-inspection pairs, test with a small `input.csv` first to ensure everything works.
- Site assignment helps with proper location tracking and reporting in SafetyCulture.
- Make sure you have authorization to modify the specified inspections.

## Data Requirements
- **audit_id**: Must be a valid SafetyCulture inspection/audit ID
- **site_id**: Must be a valid SafetyCulture site (folder) ID
- Both IDs should be in UUID format or SafetyCulture's audit ID format

For more help, consult the [SafetyCulture API documentation](https://developer.safetyculture.com/reference/inspectionsservice_setinspectionsite) or ask a colleague familiar with Python.