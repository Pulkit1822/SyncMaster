"""
This script demonstrates how to use the Google Sheets API to fetch data
from a Google Sheet.

The code does the following:

1. Creates credentials from a service account file.
2. Builds a client for the Google Sheets API using the credentials.
3. Fetches the data from the Google Sheet using the client.
4. Prints the data fetched from the Google Sheet.

The script requires the following:

* The Google Sheets API is enabled in the Google Cloud Console.
* The credentials for the service account are stored in a file named
  "credentials.json".
* The Google Sheet ID is specified in the SHEET_ID variable.
"""

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# The scopes required for the Google Sheets API.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The location of the service account credentials file.
SERVICE_ACCOUNT_FILE = 'credentials.json'

# The ID of the Google Sheet to fetch data from. replace it with yours
SHEET_ID = ''

def main():
    # Create credentials from the service account file.
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Build a client for the Google Sheets API using the credentials.
    service = build('sheets', 'v4', credentials=creds)

    # Create a resource for interacting with the Google Sheet.
    sheet = service.spreadsheets()

    # Fetch the data from the Google Sheet.
    result = sheet.values().get(spreadsheetId=SHEET_ID, range='Sheet1!A:B').execute()
    values = result.get('values', [])

    # Print the data fetched from the Google Sheet.
    if not values:
        print('No data found.')
    else:
        print('Data from Google Sheets:')
        for row in values:
            print(row)

if __name__ == '__main__':
    main()
