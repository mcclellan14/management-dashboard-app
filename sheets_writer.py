
import gspread
import streamlit as st
import json
from google.oauth2.service_account import Credentials

def write_to_google_sheets(summary_dict):
    # Load credentials from Streamlit secrets
    service_account_info = json.loads(st.secrets["GOOGLE_SHEETS_KEY"])
    creds = Credentials.from_service_account_info(service_account_info)

    # Authorize with Google Sheets
    client = gspread.authorize(creds)

    # Open the spreadsheet and select the worksheet
    spreadsheet = client.open("Management Report Dashboard")
    worksheet = spreadsheet.sheet1  # or use .worksheet("Sheet Name")

    # Convert the summary dict to a list of values (row)
    row_data = list(summary_dict.values())

    # Find the next available row
    existing_rows = worksheet.get_all_values()
    next_row = len(existing_rows) + 1

    # Insert the new row
    worksheet.insert_row(row_data, next_row)

    st.success("✅ Data pushed to Google Sheets successfully.")

