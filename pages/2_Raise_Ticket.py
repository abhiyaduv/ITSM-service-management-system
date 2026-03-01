import streamlit as st
from modules.tickets import create_ticket

# -------- LOGIN CHECK --------
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first.")
    st.stop()

st.title("🎫 Raise Ticket")

title = st.text_input("Issue Title")
description = st.text_area("Issue Description")

category = st.selectbox(
    "Category",
    ["Hardware", "Software", "Network", "Access"]
)

if st.button("Submit Ticket"):

    if title.strip() == "" or description.strip() == "":
        st.error("Please fill all fields")
    else:
        create_ticket(
            title,
            description,
            category,
            st.session_state.user["user_id"]
        )

        st.success("✅ Ticket Raised Successfully")
        st.balloons()