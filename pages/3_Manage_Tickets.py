import streamlit as st
import pandas as pd
from modules.tickets import (
    get_all_tickets_df,
    get_technicians,
    assign_ticket,
    update_ticket_status
)

# LOGIN CHECK
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

st.title("Manage Tickets")

df = get_all_tickets_df()

if df.empty:
    st.info("No tickets available")
    st.stop()

st.dataframe(df)

ticket_id = st.selectbox("Select Ticket ID", df["ticket_id"])

# ASSIGN
techs = get_technicians()

if techs:
    tech_names = [t["name"] for t in techs]
    tech_selected = st.selectbox("Assign Technician", tech_names)

    if st.button("Assign"):
        tech_id = next(t["user_id"] for t in techs if t["name"] == tech_selected)
        assign_ticket(ticket_id, tech_id)
        st.success("Assigned Successfully")
        st.rerun()

# STATUS
status = st.selectbox(
    "Update Status",
    ["Open", "Assigned", "In Progress", "Resolved", "Closed"]
)

if st.button("Update Status"):
    update_ticket_status(ticket_id, status)
    st.success("Status Updated")
    st.rerun()