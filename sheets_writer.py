import gspread
from oauth2client.service_account import ServiceAccountCredentials

def write_to_google_sheets(summary: dict):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("management-dashboard-app-de89db34c080.json", scope)

    client = gspread.authorize(creds)

    # Open your sheet by name or URL
    sheet = client.open("Management Report Dashboard").sheet1  # or .worksheet("YourTabName")

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
