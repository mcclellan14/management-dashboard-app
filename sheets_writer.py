import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Map each property to its cell range
PROPERTY_RANGES = {
    "Northland 1": "A1:G15",
    "Northland 2": "A17:G31",
    "Northland 3A&B": "A33:G47",
    "Northland 3C": "A49:G63",
    "Riverside": "A65:G79",
    "Glenmore": "A81:G95",
    "Cambrian": "A97:G111",
    "Greenview": "A113:G127",
    "Foothills": "A129:G143",
    "High River Plaza": "A145:G159",
    "Pioneer Square": "A161:G175",
    "Richfield": "A177:G191",
    "211 N Albert Street": "A193:G207",
}

def write_to_google_sheets(summary: dict):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key("1JcEi1sXNlwiCnomWK_vcYvksdhhFgkbwmwXla9q_zhI")
    worksheet = spreadsheet.sheet1

    property_name = summary.get("property")
    month = summary.get("month")

    if property_name not in PROPERTY_RANGES:
        st.error(f"❌ Unknown property: {property_name}")
        return

    range_start = PROPERTY_RANGES[property_name].split(":")[0]
    row_start = int(range_start[1:])

    # Read existing B and C columns
    existing_values = worksheet.get(PROPERTY_RANGES[property_name])
    if not existing_values or len(existing_values) < 1:
        st.error(f"❌ No existing labels found in range for {property_name}.")
        return

    # Shift column B to column C
    for i, row in enumerate(existing_values):
        if len(row) > 1:
            worksheet.update_cell(row_start + i, 3, row[1])  # C = col 3

    # Write new values to column B
    value_map = {
        "occupancy": 1,
        "net income": 2,
        "operating expenses": 3,
        "capital expenditures": 4,
        "leasing updates": 5,
        "major repairs": 6,
        "key takeaways": 7,
        "next steps": 8
    }

    worksheet.update_cell(row_start, 2, month)  # Header row gets the month in col B

    for i, key in enumerate(value_map.keys()):
        value = summary.get(key, "")
        worksheet.update_cell(row_start + i + 1, 2, value)  # B = col 2

    st.success(f"✅ Updated {property_name} data for {month} in Google Sheets.")
