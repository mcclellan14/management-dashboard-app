import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def write_to_google_sheets(summary: dict):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)

    client = gspread.authorize(creds)

    # Open your sheet by name or URL
    sheet = client.open_by_key("1JcEi1sXNlwiCnomWK_vcYvksdhhFgkbwmwXla9q_zhI").sheet1  # or .worksheet("YourTabName")

    # Build row in correct order
    row = [
        summary.get("property"),
        summary.get("month"),
        summary.get("occupancy"),
        summary.get("net income"),
        summary.get("operating expenses"),
        summary.get("capital expenditures"),
        summary.get("leasing updates"),
        summary.get("major repairs"),
        summary.get("key takeaways"),
        summary.get("next steps"),
    ]

    sheet.append_row(row, value_input_option="USER_ENTERED")
