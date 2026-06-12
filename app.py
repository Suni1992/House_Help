import json
import os
from datetime import datetime

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

st.set_page_config(
    page_title="FixMyHome",
    page_icon="🏠",
    layout="wide"
)

# -------------------
# CSS
# -------------------

st.markdown("""
<style>

.stApp{
    background:#f5f7fb;
}

.main-title{
    text-align:center;
    font-size:55px;
    font-weight:700;
}

.sub-title{
    text-align:center;
    font-size:20px;
    color:gray;
    margin-bottom:30px;
}

.service-card{
    background:white;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 3px 12px rgba(0,0,0,0.10);
}

.form-box{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.10);
}

</style>
""", unsafe_allow_html=True)

# -------------------
# HEADER
# -------------------

st.markdown(
"""
<div class="main-title">
🏠 FixMyHome
</div>

<div class="sub-title">
Book Trusted Home Service Professionals
</div>
""",
unsafe_allow_html=True
)

# -------------------
# SERVICES
# -------------------

st.subheader("Popular Services")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="service-card">
    ⚡<br><br>
    Electrician
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="service-card">
    🔧<br><br>
    Plumber
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="service-card">
    🪚<br><br>
    Carpenter
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="service-card">
    ❄️<br><br>
    AC Repair
    </div>
    """, unsafe_allow_html=True)

st.write("")

# -------------------
# Google Sheets helpers
# -------------------

def load_google_sheets_credentials():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    # 1. Prefer JSON content from an environment variable.
    account_json = "service_account.json"

    # 2. Fallback to a JSON file in the workspace.
    if not account_json:
        for path in ("service_account.json", "google_service_account.json"):
            if os.path.exists(path):
                return Credentials.from_service_account_file(path, scopes=scopes)

    # 3. Fallback to Streamlit secrets if available.
    if hasattr(st, "secrets") and st.secrets.get("google_service_account"):
        account_json = st.secrets["google_service_account"]

    if account_json:
        if isinstance(account_json, str):
            return Credentials.from_service_account_info(json.loads(account_json), scopes=scopes)
        return Credentials.from_service_account_info(account_json, scopes=scopes)

    return None


def get_google_sheet_client():
    creds = load_google_sheets_credentials()
    if creds is None:
        return None
    return gspread.authorize(creds)


def append_lead_to_sheet(sheet_id, lead_row):
    client = get_google_sheet_client()
    if client is None:
        raise RuntimeError(
            "Google Sheets credentials not found. Set GOOGLE_SERVICE_ACCOUNT_JSON or provide service_account.json."
        )

    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.sheet1
    worksheet.append_row(lead_row, value_input_option="USER_ENTERED")


st.markdown('<div class="form-box">', unsafe_allow_html=True)

st.subheader("Get Free Quote")

service = st.selectbox(
    "Service Required",
    [
        "Electrician",
        "Plumber",
        "Carpenter",
        "AC Repair",
        "Painter",
        "Cleaning"
    ]
)

col1,col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")

with col2:
    mobile = st.text_input("Mobile Number")

city = st.text_input("City")

requirement = st.text_area(
    "Describe Your Requirement",
    height=120
)

submit = st.button(
    "🚀 Get Free Quotes",
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------
# SAVE LEAD
# -------------------

if submit:

    if not name or not mobile or not city:

        st.error("Please fill all mandatory fields.")

    else:

        lead = pd.DataFrame([{
            "Date":datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Service":service,
            "Name":name,
            "Mobile":mobile,
            "City":city,
            "Requirement":requirement,
            "Status":"New"
        }])

        file_name = "leads.csv"

        if os.path.exists(file_name):
            lead.to_csv(
                file_name,
                mode="a",
                header=False,
                index=False
            )
        else:
            lead.to_csv(
                file_name,
                index=False
            )

        spreadsheet_id = os.getenv("1NXR6PSGa7DVwvPfcWgf8fqH9HxNe5F9up0pB07rFLSE")
        
        if not spreadsheet_id:
            try:
                spreadsheet_id = st.secrets.get("google_sheets_spreadsheet_id")
            except Exception:
                spreadsheet_id = None

        if spreadsheet_id:
            try:
                append_lead_to_sheet(
                    spreadsheet_id,
                    [
                        datetime.now().strftime("%d-%m-%Y %H:%M"),
                        service,
                        name,
                        mobile,
                        city,
                        requirement,
                        "New",
                    ],
                )
                st.success(
                    "✅ Request Submitted Successfully. We will contact you shortly."
                )
                st.info("Google Sheet updated successfully.")
            except Exception as gsheet_error:
                st.warning(
                    "Saved locally, but Google Sheets sync failed. Check credentials and sheet ID."
                )
                st.error(str(gsheet_error))
        else:
            st.success(
                "✅ Request Submitted Successfully. We will contact you shortly."
            )
            st.info(
                "To sync leads to Google Sheets, set GOOGLE_SHEETS_SPREADSHEET_ID and Google credentials."
            )

# -------------------
# TRUST SECTION
# -------------------

st.write("")
st.write("")

a,b,c = st.columns(3)

with a:
    st.metric("Verified Professionals", "500+")

with b:
    st.metric("Customers Served", "10,000+")

with c:
    st.metric("Cities Covered", "15+")

st.write("")
st.write("")

st.markdown(
"""
<center>
© 2026 FixMyHome
</center>
""",
unsafe_allow_html=True
)
