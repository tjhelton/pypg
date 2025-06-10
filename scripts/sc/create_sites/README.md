# SafetyCulture Site Creator

This Python script creates sites in SafetyCulture via API. It reads site details (name and optional parent ID) from a CSV file, sends creation requests to the SafetyCulture API, and logs the results to an output CSV file. This guide is for beginners to Python who want to run the script.

## Prerequisites
- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org/downloads/) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.
- **Input CSV File**: Create a CSV file named `input.csv` with columns for site names and optional parent IDs.

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
   - The CSV should have a `name` column for site names, a `meta_label` column for site level, and an optional `parent` column for parent IDs (leave blank if not needed). For example:
     ```
     name,meta_label,parent
     Site A,area,
     Site B,location,site_123456
     Site C,location,site_789012
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
   - Read site details from `input.csv`.
   - Send site creation requests to the SafetyCulture API for each site.
   - Save the results to a file named `output.csv`.

## Output
- After running, check the `output.csv` file in the same folder. It will contain:
  - A `count` column for the order of processing.
  - A `site_name` column for the site name.
  - A `meta_label` column (if provided in the input CSV).
  - A `status` column with the API response or error message for each site.

## Troubleshooting
- **Error: "No module named pandas" or "No module named requests"**
  - Ensure you ran `pip install pandas requests`.
- **Error: "File input.csv not found"**
  - Make sure `input.csv` is in the same folder as the script and is correctly formatted.
- **API Errors**
  - Check that your API token is correct and valid.
  - Ensure the site names and parent IDs in `input.csv` are correct and valid.
- **Permission Issues**
  - If you get permission errors, try running the terminal as an administrator (Windows) or with `sudo` (macOS/Linux).

## Notes
- The script uses the SafetyCulture API endpoint for creating sites (`https://api.safetyculture.io/directory/v1/folder`). Verify the API documentation if you encounter issues.
- Keep your API token secure and do not share it publicly.
- If you need to create many sites, test with a small `input.csv` first to ensure everything works.
- Parent IDs must correspond to existing sites in SafetyCulture if provided.

For more help, consult the [SafetyCulture API documentation](https://developer.safetyculture.com/reference/directory_createfolder) or ask a colleague familiar with Python.