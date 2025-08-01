import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Define where each property's data goes
PROPERTY_CELL_RANGES = {
    "Northland 1": (1, 15),
    "Northland 2": (17, 31),
    "Northland 3A&B": (33, 47),
    "Northland 3C": (49, 63),
    "Riverside": (65, 79),
    "Glenmore": (81, 95),
    "Cambrian": (97, 111),
    "Greenview": (113, 127),
    "Foothills": (129, 143),
    "High River Plaza": (145, 159),
    "Pioneer Square": (161, 175),
    "Richfield": (177, 191),
    "211 N Albert Street": (193, 207),
}

ROW_MAPPING = {
    "occupancy": 0,
    "operating expenses": 1,
    "capital expenditures": 2,
    "net income": 3,
    "leasing updates": 4,
    "major repairs": 5,
    "key takeaways": 6,
    "next steps": 7,
}

def write_to_google_sheets(summary: dict):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope
    )
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1JcEi1sXNlwiCnomWK_vcYvksdhhFgkbwmwXla9q_zhI").sheet1

    property_name = summary.get("property")
    month = summary.get("month")

    if property_name not in PROPERTY_CELL_RANGES:
        st.warning(f"Unknown property: {property_name}")
        return

    start_row, end_row = PROPERTY_CELL_RANGES[property_name]

    for key, row_offset in ROW_MAPPING.items():
        value = summary.get(key, "")
        if value:
            target_row = start_row + row_offset

            # Shift current B to C (i.e., preserve previous month)
            old_value = sheet.cell(target_row + 1, 2).value  # B column
            if old_value:
                sheet.update_cell(target_row + 1, 3, old_value)  # move to column C

            # Write new value to column B
            sheet.update_cell(target_row + 1, 2, value)  # row is 1-indexed
