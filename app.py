import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="FixMyHome",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# DATABASE
# -----------------------------
conn = sqlite3.connect("leads.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    service TEXT,
    name TEXT,
    mobile TEXT,
    city TEXT,
    requirement TEXT,
    status TEXT
)
""")

conn.commit()

# -----------------------------
# HEADER
# -----------------------------
st.title("🏠 FixMyHome")
st.subheader("Find Trusted Home Service Professionals")

st.write(
    """
    Book verified professionals for:
    - Electrician
    - Plumber
    - Carpenter
    - AC Repair
    - Painter
    - Cleaning
    """
)

# -----------------------------
# LEAD FORM
# -----------------------------
with st.form("lead_form"):

    service = st.selectbox(
        "Select Service",
        [
            "Electrician",
            "Plumber",
            "Carpenter",
            "AC Repair",
            "Painter",
            "Cleaning"
        ]
    )

    name = st.text_input("Full Name")

    mobile = st.text_input("Mobile Number")

    city = st.text_input("City")

    requirement = st.text_area(
        "Describe Your Requirement"
    )

    submit = st.form_submit_button(
        "🚀 Get Free Quotes"
    )

# -----------------------------
# SAVE DATA
# -----------------------------
if submit:

    if not name:
        st.error("Please enter name")

    elif not mobile:
        st.error("Please enter mobile number")

    elif len(mobile) != 10:
        st.error("Mobile number must be 10 digits")

    else:

        cursor.execute("""
        INSERT INTO leads (
            created_at,
            service,
            name,
            mobile,
            city,
            requirement,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime("%d-%m-%Y %H:%M"),
            service,
            name,
            mobile,
            city,
            requirement,
            "New"
        ))

        conn.commit()

        st.success(
            "✅ Thank you! Your request has been submitted."
        )

# -----------------------------
# ADMIN PANEL
# -----------------------------
st.divider()

st.subheader("📋 All Leads")

try:
    leads = pd.read_sql_query(
        "SELECT * FROM leads ORDER BY id DESC",
        conn
    )

    st.dataframe(
        leads,
        use_container_width=True
    )

    st.write(f"Total Leads: {len(leads)}")

except Exception as e:
    st.error(str(e))

# -----------------------------
# DOWNLOAD
# -----------------------------
if 'leads' in locals():

    csv = leads.to_csv(index=False)

    st.download_button(
        "⬇ Download Leads CSV",
        csv,
        file_name="FixMyHome_Leads.csv",
        mime="text/csv"
    )