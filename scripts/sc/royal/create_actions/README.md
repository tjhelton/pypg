# SafetyCulture Bulk Action Creator

This Python script creates actions in bulk in SafetyCulture via API. It reads action details from a CSV file (`assets.csv`), sends creation requests to the SafetyCulture API, and logs the results to an output CSV file (`output.csv`). The script includes retry logic for handling API errors and generates unique action IDs for each action. This guide is for beginners to Python who want to run the script.

## Prerequisites
- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org/downloads/) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.
- **Input CSV File**: Create a CSV file named `assets.csv` with columns for action details.

## Setup Instructions

1. **Install Python**
   - Download and install Python 3 from [python.org](https://www.python.org/downloads/).
   - During installation, check the box to add Python to your PATH (this makes it easier to run Python from the command line).

2. **Install Required Libraries**
   - Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux).
   - Run the following command to install the required Python libraries:
     ```bash
     pip install pandas requests
     ```
   - This installs `pandas` (for handling CSV files) and `requests` (for making API calls).

3. **Prepare the Input CSV File**
   - Create a file named `assets.csv` in the same folder as the script.
   - The CSV should have the following columns:
     - `title`: The title of the action.
     - `description`: The description of the action.
     - `assignee`: The group UUID for the assignee.
     - `site_uuid`: The site ID where the action will be created.
     - `asset_id`: The asset ID associated with the action.
     - `label_id`: The label ID for the action.
     - `frequency`: The recurrence rule (RRULE) for the action schedule (e.g., `FREQ=DAILY`).
     - `template_id`: The template ID for the action.
   - Example `assets.csv`:
     ```csv
     title,description,assignee,site_uuid,asset_id,label_id,frequency,template_id
     "Inspect Machine A","Check machine status","group_123456","site_789012","asset_345678","label_901234","FREQ=DAILY","template_567890"
     "Clean Equipment B","Clean daily","group_234567","site_789012","asset_456789","label_012345","FREQ=WEEKLY","template_678901"
     ```
   - Save the file as `assets.csv`. You can create it in a text editor or a spreadsheet program like Excel.

4. **Add Your API Token**
   - Open the script file (e.g., `main.py`) in a text editor.
   - Find the line `TOKEN = ''` near the top.
   - Replace `''` with your SafetyCulture API token, like this:
     ```python
     TOKEN = 'your-api-token-here'
     ```
   - Save the script.

## Running the Script

1. Open a terminal and navigate to the folder containing `main.py` and `assets.csv`. For example:
   ```bash
   cd path/to/your/folder

   (Replace path/to/your/folder with the actual path.)

Run the script by typing:
python main.py


The script will:

Read action details from assets.csv.
Generate a unique action ID for each action.
Send action creation requests to the SafetyCulture API for each action.
Log the results to output.csv.
Print progress and API response statuses to the console.



Output

After running, check the output.csv file in the same folder. It will contain:
action_id: The unique ID generated for the action.
asset_id: The asset ID from the input CSV.
title: The action title.
status: Either SUCCESS or ERROR based on the API response.
message: Additional details, such as error messages if the action creation failed.


The console will display progress (e.g., "Processing action 1/2: Inspect Machine A...") and API response statuses.

Troubleshooting

Error: "No module named pandas" or "No module named requests"
Ensure you ran pip install pandas requests.


Error: "File assets.csv not found"
Make sure assets.csv is in the same folder as the script and is correctly formatted.


API Errors
Check that your API token is correct and valid.
Ensure all required fields in assets.csv (e.g., title, assignee, site_uuid, asset_id, label_id, frequency, template_id) are correct and correspond to existing entities in SafetyCulture.
Verify the RRULE format for frequency (e.g., FREQ=DAILY, FREQ=WEEKLY) matches SafetyCulture's API requirements.


Permission Issues
If you get permission errors, try running the terminal as an administrator (Windows) or with sudo (macOS/Linux).


Retry Failures
The script retries failed API requests up to 3 times with increasing delays. If all retries fail, check the API endpoint and payload in the console output for debugging.



Notes

The script uses the SafetyCulture API endpoint for creating action schedules (https://api.safetyculture.io/tasks/v1/actions:CreateActionSchedule). Verify the API documentation if you encounter issues.
Keep your API token secure and do not share it publicly.
Test with a small assets.csv file first to ensure everything works, especially if creating many actions.
The script includes retry logic (3 attempts with exponential backoff) to handle temporary API issues.
Ensure all UUIDs (e.g., assignee, site_uuid, asset_id, label_id, template_id) are valid and exist in SafetyCulture.

For more help, consult the SafetyCulture API documentation or ask a colleague familiar with Python.```