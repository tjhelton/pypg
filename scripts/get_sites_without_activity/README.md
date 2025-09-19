# SafetyCulture Sites Without Activity Finder

This Python script identifies SafetyCulture sites (locations) that have no inspection activity by fetching all sites and inspections, then comparing them to find inactive sites. The script generates three CSV reports for analysis. This guide is for beginners to Python who want to run the script.

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
     pip install pandas requests
     ```
   - This installs `pandas` (for handling CSV files) and `requests` (for making API calls).

3. **Add Your API Token**
   - Open the script file (e.g., `main.py`) in a text editor.
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
   - Fetch all sites from your SafetyCulture organization.
   - Fetch all inspections from your SafetyCulture organization.
   - Compare sites and inspections to identify sites without activity.
   - Display progress messages in the terminal.
   - Generate three CSV output files.

## Output Files
The script generates three CSV files:

1. **`sites.csv`**: Contains all sites in your organization
   - Includes all site metadata and properties

2. **`inspections.csv`**: Contains all inspections in your organization
   - Includes inspection metadata and associated site information

3. **`no_inspection_activity.csv`**: Contains sites with no inspection activity
   - These are sites that exist but have never had any inspections conducted

## Troubleshooting
- **Error: "No module named pandas" or "No module named requests"**
  - Ensure you ran `pip install pandas requests`.
- **API Errors**
  - Check that your API token is correct and valid.
  - Ensure you have permissions to access sites and inspections data.
- **Permission Issues**
  - If you get permission errors, try running the terminal as an administrator (Windows) or with `sudo` (macOS/Linux).
- **Large Dataset Issues**
  - For organizations with many sites/inspections, the script may take several minutes to complete.
  - The script will show progress messages indicating how many records have been fetched.

## Use Cases
- **Site Cleanup**: Identify and potentially remove unused sites
- **Usage Analysis**: Understand which locations are actively being inspected
- **Resource Planning**: Focus inspection resources on active sites
- **Data Quality**: Clean up your site directory by removing inactive locations
- **Compliance Reporting**: Ensure all required sites have inspection activity

## Notes
- The script fetches ALL sites and inspections, which may take time for large organizations.
- Only leaf node sites (sites without child sites) are included in the analysis.
- The script considers ANY inspection activity - completed or in-progress.
- Keep your API token secure and do not share it publicly.
- Review the results carefully before taking any action on inactive sites.

## Additional Features
The script also includes helper functions for:
- Deleting sites (use with extreme caution)
- Getting detailed inspection information
- Checking site status (active/deleted)

For more help, consult the [SafetyCulture API documentation](https://developer.safetyculture.com/) or ask a colleague familiar with Python.