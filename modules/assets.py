from database import get_connection
import pandas as pd
from datetime import datetime


# ---------- ADD ASSET ----------
def add_asset(asset_name, asset_type):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assets
        (asset_name, asset_type, status, assigned_to, purchase_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        asset_name,
        asset_type,
        "Available",
        None,
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()


# ---------- GET ALL ASSETS ----------
def get_assets():

    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT 
            asset_id,
            asset_name,
            asset_type,
            status,
            assigned_to,
            purchase_date
        FROM assets
        ORDER BY asset_id DESC
    """, conn)

    conn.close()
    return df


# ---------- GET USERS ----------
def get_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, name FROM users")
    users = cursor.fetchall()

    conn.close()
    return users


# ---------- ASSIGN ASSET ----------
def assign_asset(asset_id, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE assets
        SET assigned_to=?, status='Assigned'
        WHERE asset_id=?
    """, (user_id, asset_id))

    conn.commit()
    conn.close()


# ---------- UPDATE STATUS ----------
def update_asset_status(asset_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE assets
        SET status=?
        WHERE asset_id=?
    """, (status, asset_id))

    conn.commit()
    conn.close()


# ---------- DELETE ASSET ----------
def delete_asset(asset_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM assets WHERE asset_id=?", (asset_id,))

    conn.commit()
    conn.close()