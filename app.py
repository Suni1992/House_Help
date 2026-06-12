import streamlit as st
import pandas as pd
import os
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="FixMyHome",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# CSV FILE
# -----------------------------
CSV_FILE = "leads.csv"

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=[
        "Date",
        "Service",
        "Name",
        "Mobile",
        "City",
        "Requirement",
        "Status"
    ]).to_csv(CSV_FILE, index=False)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main-title{
    text-align:center;
    color:#ff6b00;
    font-size:48px;
    font-weight:bold;
}
.sub-title{
    text-align:center;
    font-size:20px;
    margin-bottom:30px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<p class="main-title">🏠 FixMyHome</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Book Trusted Home Service Professionals</p>',
    unsafe_allow_html=True
)

# -----------------------------
# SERVICES
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.info("⚡ Electrician")

with col2:
    st.info("🚿 Plumber")

with col3:
    st.info("🪚 Carpenter")

col4, col5, col6 = st.columns(3)

with col4:
    st.info("❄️ AC Repair")

with col5:
    st.info("🎨 Painter")

with col6:
    st.info("🧹 Cleaning")

st.markdown("---")

# -----------------------------
# LEAD FORM
# -----------------------------
st.subheader("Get Free Quotes")

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
        "🚀 Submit Request"
    )

# -----------------------------
# SAVE LEAD
# -----------------------------
if submit:

    if name.strip() == "":
        st.error("Please enter your name")

    elif mobile.strip() == "":
        st.error("Please enter mobile number")

    elif not mobile.isdigit():
        st.error("Mobile number must contain digits only")

    elif len(mobile) != 10:
        st.error("Mobile number must be 10 digits")

    else:

        lead = pd.DataFrame([{
            "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Service": service,
            "Name": name,
            "Mobile": mobile,
            "City": city,
            "Requirement": requirement,
            "Status": "New"
        }])

        lead.to_csv(
            CSV_FILE,
            mode="a",
            header=False,
            index=False
        )

        st.success(
            "✅ Thank you! Your request has been submitted successfully."
        )

        st.balloons()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("© 2026 FixMyHome. All Rights Reserved.")