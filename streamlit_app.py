
import streamlit as st
import pdfplumber
import pandas as pd
from extract_summary import extract_summary
from sheets_writer import write_to_google_sheets

st.set_page_config(page_title="Management Report Dashboard", layout="wide")
st.title("📊 Management Report Summary Tool")

uploaded_files = st.file_uploader(
    "Upload one or more management reports (PDF)",
    type="pdf",
    accept_multiple_files=True
)

summary_rows = []

if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"📄 {file.name}")

        with pdfplumber.open(file) as pdf:
            full_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

        # Extract month from filename if possible
        if "may" in file.name.lower():
            report_month = "May 2025"
        elif "apr" in file.name.lower():
            report_month = "April 2025"
        else:
            report_month = "Unknown"

        summary = extract_summary(full_text, report_month)

        # Display as a mini table
        st.write(pd.DataFrame.from_dict(summary, orient="index", columns=["Value"]))

        summary_rows.append(summary)

    # Optional: show all summaries together
    if len(summary_rows) > 1:
        st.markdown("### All Summaries")
        st.dataframe(pd.DataFrame(summary_rows))

    # Push to Google Sheets button
        # Push to Google Sheets button
    if st.button("Push to Google Sheets"):
        try:
            for summary in summary_rows:
                write_to_google_sheets(summary)
            st.success("✅ Data successfully pushed to Google Sheets.")
        except Exception as e:
            st.error(f"❌ Failed to push data: {e}")


