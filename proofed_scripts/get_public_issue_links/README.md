# SafetyCulture Public Issue Link Generator

This Python script generates public web report links for SafetyCulture issues (tasks) in bulk using the SafetyCulture API. It reads issue IDs from a CSV file, creates shareable public links for each issue via API calls, and logs the results to an output CSV file. This guide is for beginners to Python who want to run the script.

## Prerequisites
- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org/downloads/) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.
- **Input CSV File**: Create a CSV file named `input.csv` with issue IDs for which you want to generate public links.

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
   - The CSV should have an `issue_id` column with issue IDs. For example:
     ```
     issue_id
     audit_f47ac10b58cc4372a5670e02b2c3d479
     audit_f47ac10b58cc4372a5670e02b2c3d480
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
   - Read issue IDs from `input.csv`.
   - Generate public web report links for each issue via SafetyCulture API calls.
   - Display progress messages in the terminal.
   - Save the results to a file named `output.csv`.

## Output
- After running, check the `output.csv` file in the same folder. It will contain:
  - A column for the `issue_id` that was processed.
  - A column for the `url` containing the public link (or "N/A" if failed).
  - A column for the `status` showing success or error messages.

## Troubleshooting
- **Error: "No module named pandas" or "No module named requests"**
  - Ensure you ran `pip install pandas requests`.
- **Error: "File input.csv not found"**
  - Make sure `input.csv` is in the same folder as the script and is correctly formatted.
- **API Errors**
  - Check that your API token is correct and valid.
  - Ensure you have permissions to access and share the issues.
  - Verify that the issue IDs exist and are correct.
- **Permission Issues**
  - If you get permission errors, try running the terminal as an administrator (Windows) or with `sudo` (macOS/Linux).

## Notes
- The script generates public links sequentially and logs all results.
- Keep your API token secure and do not share it publicly.
- Public links allow anyone with the URL to view the issue report without authentication.
- Make sure you have authorization to create public links for the specified issues.
- If generating many links, test with a small `input.csv` first to ensure everything works.

## Use Cases
- Sharing inspection reports with external stakeholders
- Creating public access to audit findings
- Generating links for regulatory compliance reporting
- Providing access to contractors or clients

For more help, consult the [SafetyCulture API documentation](https://developer.safetyculture.com/reference/tasksservice_createsharedlink) or ask a colleague familiar with Python.