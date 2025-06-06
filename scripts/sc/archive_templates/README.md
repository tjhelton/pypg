# SafetyCulture Template Archiver

This Python script archives templates in SafetyCulture using their API. It reads template IDs from a CSV file, sends archive requests to the SafetyCulture API, and logs the results to an output CSV file. This guide is for beginners to Python who want to run the script.

## Prerequisites
- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org/downloads/) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.
- **Input CSV File**: Create a CSV file named `input.csv` with a column containing the template IDs you want to archive.

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
   - The CSV should have at least one column with template IDs. For example:
     ```
     template_id
     template_123456
     template_789012
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
   python archive_templates.py
   ```

3. The script will:
   - Read template IDs from `input.csv`.
   - Send archive requests to the SafetyCulture API for each template ID.
   - Save the results to a file named `log_output.csv`.

## Output
- After running, check the `log_output.csv` file in the same folder. It will contain:
  - A column for the `template_id` processed.
  - A column for the `result` (the API response for each template).

## Troubleshooting
- **Error: "No module named pandas" or "No module named requests"**
  - Ensure you ran `pip install pandas requests`.
- **Error: "File input.csv not found"**
  - Make sure `input.csv` is in the same folder as the script and is correctly formatted.
- **API Errors**
  - Check that your API token is correct and valid.
  - Ensure the template IDs in `input.csv` are correct.
- **Permission Issues**
  - If you get permission errors, try running the terminal as an administrator (Windows) or with `sudo` (macOS/Linux).

## Notes
- The script assumes the SafetyCulture API endpoint and token format are correct. Verify the API documentation if you encounter issues.
- Keep your API token secure and do not share it publicly.
- If you need to archive many templates, test with a small `input.csv` first to ensure everything works.

For more help, consult the [SafetyCulture API documentation](https://developer.safetyculture.com/reference/templatesservice_archivetemplate) or ask a colleague familiar with Python.