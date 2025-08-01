import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def write_to_google_sheets(summary: dict):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = st.secrets["gcp_service_account"]

    # Print to check basic credential fields (harmless fields only)
    st.write("Loaded credentials for:", creds_dict.get("client_email"))
    st.write("Project ID:", creds_dict.get("project_id"))

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Try listing files to check if auth works at all
    try:
        st.write("Attempting to list accessible spreadsheets...")
        spreadsheet_list = client.openall()
        st.write(f"Found {len(spreadsheet_list)} spreadsheets.")
    except Exception as e:
        st.error(f"Credential test failed: {e}")
        return

    # Continue to open target sheet
    sheet = client.open_by_key("1JcEi1sXNlwiCnomWK_vcYvksdhhFgkbwmwXla9q_zhI").sheet1

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

