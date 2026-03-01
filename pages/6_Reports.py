import streamlit as st
import pandas as pd
from modules.reports import (
    get_ticket_report,
    get_asset_report,
    get_sla_breach_report
)

# -------- LOGIN CHECK --------
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

st.title("📊 ITSM Reports Center")

report_type = st.selectbox(
    "Select Report Type",
    ["Ticket Report", "Asset Report", "SLA Breach Report"]
)

# =============================
# TICKET REPORT
# =============================
if report_type == "Ticket Report":

    st.subheader("🎫 Ticket Report")

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Open", "Assigned", "In Progress", "Resolved", "Closed"]
    )

    category_filter = st.selectbox(
        "Filter by Category",
        ["All", "Hardware", "Software", "Network", "Access"]
    )

    df = get_ticket_report(status_filter, category_filter)

    if df.empty:
        st.info("No records found")
    else:
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            csv,
            "ticket_report.csv",
            "text/csv"
        )

# =============================
# ASSET REPORT
# =============================
elif report_type == "Asset Report":

    st.subheader("🖥 Asset Report")

    df = get_asset_report()

    if df.empty:
        st.info("No assets found")
    else:
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            csv,
            "asset_report.csv",
            "text/csv"
        )

# =============================
# SLA BREACH REPORT
# =============================
elif report_type == "SLA Breach Report":

    st.subheader("⏱ SLA Breach Report")

    df = get_sla_breach_report()

    if df.empty:
        st.success("No SLA breaches 🎉")
    else:
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            csv,
            "sla_breach_report.csv",
            "text/csv"
        )