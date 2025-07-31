
=======
def write_to_google_sheets(summary: dict):
    """
    Mocked write function — logs where data would go in Google Sheets.
    Replace with real gspread logic after validation.
    """
    property_name = summary.get("property")
    month = summary.get("month")
    print(f"\n--- Writing to Google Sheets ---")
    print(f"Property: {property_name}")
    print(f"Month: {month}")

    for key, value in summary.items():
        if key not in ["property", "month"]:
            print(f"  Would write: {key} = {value}")

    print("--- End Write Preview ---\n")
>>>>>>> 02f13592a74ec1e55e2efe21ec6d61930c5e30ed
