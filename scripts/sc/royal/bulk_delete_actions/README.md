# SafetyCulture Bulk Action Deleter

This Python script deletes actions in bulk in SafetyCulture via API. It reads action IDs from a CSV file, chunks them into groups of 300 to respect potential API limits, sends deletion requests to the SafetyCulture API, and prints the responses to the console. This guide is for beginners to Python who want to run the script.

## Prerequisites
- **Python 3**: You need Python installed on your computer. Download it from [python.org](https://www.python.org/downloads/) if you don't have it.
- **pip**: This comes with Python and is used to install required libraries.
- **SafetyCulture API Token**: You need a valid API token from SafetyCulture. Replace the empty `TOKEN = ''` in the script with your token.
- **Input CSV File**: Create a CSV file named `input.csv` with a column for action IDs.

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
   - Create a file named `input.csv` in the same folder as the script.
   - The CSV should have an `id` column for action IDs. For example:
     ```csv
     id
     action_123456
     action_789012
     action_345678
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
   ```bash
   cd path/to/your/folder

   (Replace path/to/your/folder with the actual path.)

Run the script by typing:
python main.py


The script will:

Read action IDs from input.csv.
Chunk the IDs into groups of 300.
Send deletion requests to the SafetyCulture API for each chunk.
Print the API responses to the console.



Output

The script prints the response from the API for each chunk of deletions directly to the console. Successful deletions might show a confirmation message, while errors will include details from the API.

Troubleshooting

Error: "No module named pandas" or "No module named requests"
Ensure you ran pip install pandas requests.


Error: "File input.csv not found"
Make sure input.csv is in the same folder as the script and is correctly formatted.


API Errors
Check that your API token is correct and valid.
Ensure the action IDs in input.csv are correct and correspond to existing actions in SafetyCulture.


Permission Issues
If you get permission errors, try running the terminal as an administrator (Windows) or with sudo (macOS/Linux).



Notes

The script uses the SafetyCulture API endpoint for deleting actions (https://api.safetyculture.io/tasks/v1/actions/delete). Verify the API documentation if you encounter issues.
Keep your API token secure and do not share it publicly.
Deletions are permanent—back up any important data before running the script.
If you need to delete many actions, test with a small input.csv first to ensure everything works.
The chunk size of 300 is used to avoid overwhelming the API; adjust if needed based on API limits.

For more help, consult the SafetyCulture API documentation or ask a colleague familiar with Python.```