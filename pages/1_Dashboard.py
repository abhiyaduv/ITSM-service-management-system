import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection

# LOGIN CHECK
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

st.title("📊 ITSM Analytics Dashboard")

conn = get_connection()

df = pd.read_sql_query("SELECT * FROM tickets", conn)
users = pd.read_sql_query("SELECT * FROM users", conn)

conn.close()

if df.empty:
    st.info("No tickets available")
    st.stop()

# ---------------- KPI SECTION ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tickets", len(df))
col2.metric("Open Tickets", len(df[df["status"] == "Open"]))
col3.metric("Resolved Tickets", len(df[df["status"] == "Resolved"]))
col4.metric("Closed Tickets", len(df[df["status"] == "Closed"]))

st.divider()

# ---------------- STATUS CHART ----------------
status_chart = px.pie(
    df,
    names="status",
    title="Tickets by Status"
)

st.plotly_chart(status_chart, use_container_width=True)

# ---------------- CATEGORY CHART ----------------
category_chart = px.bar(
    df,
    x="category",
    title="Tickets by Category",
)

st.plotly_chart(category_chart, use_container_width=True)

# ---------------- PRIORITY CHART ----------------
priority_chart = px.histogram(
    df,
    x="priority",
    title="Priority Distribution"
)

st.plotly_chart(priority_chart, use_container_width=True)

# ---------------- TECHNICIAN WORKLOAD ----------------
if "assigned_to" in df.columns:
    workload = df.groupby("assigned_to").size().reset_index(name="count")

    if not workload.empty:
        tech_chart = px.bar(
            workload,
            x="assigned_to",
            y="count",
            title="Technician Workload"
        )
        st.plotly_chart(tech_chart, use_container_width=True)