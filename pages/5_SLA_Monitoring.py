import streamlit as st
import pandas as pd
from database import get_connection
from datetime import datetime

# LOGIN CHECK
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

st.title("⏱ SLA Monitoring Dashboard")

conn = get_connection()
df = pd.read_sql_query("SELECT * FROM tickets", conn)
conn.close()

if df.empty:
    st.info("No tickets available")
    st.stop()

df["sla_deadline"] = pd.to_datetime(df["sla_deadline"])
df["created_date"] = pd.to_datetime(df["created_date"])

# Calculate remaining time
df["Remaining_Time"] = df["sla_deadline"] - datetime.now()

def calculate_sla_status(row):
    if row["status"] == "Closed":
        return "Closed"
    elif row["Remaining_Time"].total_seconds() < 0:
        return "Breached"
    else:
        return "Within SLA"

df["SLA_Status"] = df.apply(calculate_sla_status, axis=1)

# KPI SECTION
total = len(df)
breached = len(df[df["SLA_Status"] == "Breached"])
within = len(df[df["SLA_Status"] == "Within SLA"])
closed = len(df[df["SLA_Status"] == "Closed"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", total)
col2.metric("Within SLA", within)
col3.metric("Breached", breached)
col4.metric("Closed", closed)

st.divider()

# SLA Compliance %
if total > 0:
    compliance = ((within + closed) / total) * 100
    st.progress(int(compliance))
    st.write(f"SLA Compliance: {compliance:.2f}%")

st.divider()

st.subheader("Detailed SLA View")

st.dataframe(
    df[[
        "ticket_id",
        "priority",
        "status",
        "sla_deadline",
        "Remaining_Time",
        "SLA_Status"
    ]],
    use_container_width=True
)