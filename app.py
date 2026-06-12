import os
from datetime import datetime

import pandas as pd
import streamlit as st

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(SCRIPT_DIR, "leads.csv")

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

        if os.path.exists(CSV_FILE_PATH):
            lead.to_csv(
                CSV_FILE_PATH,
                mode="a",
                header=False,
                index=False
            )
        else:
            lead.to_csv(
                CSV_FILE_PATH,
                index=False
            )

        st.success(
            "✅ Request Submitted Successfully. We will contact you shortly."
        )
        st.info("Your request has been saved and we will contact you soon.")

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
