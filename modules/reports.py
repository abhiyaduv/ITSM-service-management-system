from database import get_connection
import pandas as pd
from datetime import datetime


# ---------------- TICKET REPORT ----------------
def get_ticket_report(status=None, category=None):

    conn = get_connection()

    query = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if status and status != "All":
        query += " AND status=?"
        params.append(status)

    if category and category != "All":
        query += " AND category=?"
        params.append(category)

    df = pd.read_sql_query(query, conn, params=params)

    conn.close()
    return df


# ---------------- ASSET REPORT ----------------
def get_asset_report():

    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT * FROM assets
        ORDER BY asset_id DESC
    """, conn)

    conn.close()
    return df


# ---------------- SLA BREACH REPORT ----------------
def get_sla_breach_report():

    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT * FROM tickets
    """, conn)

    conn.close()

    if df.empty:
        return df

    df["sla_deadline"] = pd.to_datetime(df["sla_deadline"])

    breached = df[
        (df["sla_deadline"] < datetime.now()) &
        (df["status"] != "Closed")
    ]

    return breached