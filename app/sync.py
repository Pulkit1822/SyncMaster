"""
This module contains functions to synchronize data between a Google Sheets
spreadsheet and a MySQL database.

The `sync_with_google_sheet` function fetches data from a Google Sheets
spreadsheet and inserts it into the MySQL database.

The `update_google_sheet` function fetches data from the MySQL database and
updates the Google Sheets spreadsheet.
"""

import logging
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from app import db

# The scope for the Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The file containing the service account credentials
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Set up logging to see what's going on
logging.basicConfig(level=logging.DEBUG)


def sync_with_google_sheet(sheet_id):
    """
    Synchronize data from a Google Sheets spreadsheet to the MySQL database.

    Args:
        sheet_id (str): The ID of the Google Sheets spreadsheet to synchronize
            with.

    Returns:
        None
    """
    logging.debug("Starting synchronization with Google Sheets")

    # Create credentials for the Google Sheets API
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Create the Google Sheets API client
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Fetch data from Google Sheets
    result = sheet.values().get(spreadsheetId=sheet_id, range='Sheet1!A:B').execute()
    values = result.get('values', [])

    if not values:
        logging.debug("No data found in Google Sheets")
    else:
        logging.debug(f"Data fetched from Google Sheets: {values}")

    # Sync with MySQL
    cursor = db.cursor()
    cursor.execute("DELETE FROM data")  # Clear existing data
    for row in values:
        name, value = row[0], row[1]
        cursor.execute("INSERT INTO data (name, value) VALUES (%s, %s)", (name, value))
    db.commit()
    logging.debug("Data synchronized with MySQL")


def update_google_sheet(sheet_id):
    """
    Update a Google Sheets spreadsheet with data from the MySQL database.

    Args:
        sheet_id (str): The ID of the Google Sheets spreadsheet to update.

    Returns:
        None
    """
    logging.debug("Updating Google Sheets with data from MySQL")

    # Create credentials for the Google Sheets API
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Create the Google Sheets API client
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Fetch data from MySQL
    cursor = db.cursor()
    cursor.execute("SELECT name, value FROM data")
    rows = cursor.fetchall()

    # Prepare data for Google Sheets
    values = [[row[0], row[1]] for row in rows]

    # Update Google Sheets
    body = {
        'values': values
    }
    result = sheet.values().update(
        spreadsheetId=sheet_id,
        range='Sheet1!A:B',
        valueInputOption='RAW',
        body=body
    ).execute()

    logging.debug(f"Google Sheets updated: {result.get('updatedCells')} cells updated")
