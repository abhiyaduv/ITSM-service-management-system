from database import get_connection
from datetime import datetime
import pandas as pd
from datetime import datetime, timedelta


def calculate_priority(category):
    if category == "Network":
        return "High"
    elif category == "Hardware":
        return "Medium"
    else:
        return "Low"


def calculate_sla_deadline(priority):
    now = datetime.now()

    if priority == "High":
        return now + timedelta(hours=4)
    elif priority == "Medium":
        return now + timedelta(hours=8)
    else:
        return now + timedelta(hours=24)


def create_ticket(title, description, category, user_id):

    priority = calculate_priority(category)
    deadline = calculate_sla_deadline(priority)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets
        (title, description, category, priority, status, created_date, assigned_to, sla_deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        category,
        priority,
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        None,
        deadline.strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

# ---------- CREATE TICKET ----------
def create_ticket(title, description, category, user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets
        (title, description, category, priority, status, created_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        category,
        "Low",
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        None
    ))

    conn.commit()
    conn.close()


# ---------- GET ALL TICKETS ----------
def get_all_tickets_df():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT 
            ticket_id,
            title,
            category,
            priority,
            status,
            created_date,
            assigned_to
        FROM tickets
        ORDER BY ticket_id DESC
    """, conn)

    conn.close()
    return df


# ---------- GET TECHNICIANS ----------
def get_technicians():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, name FROM users WHERE role='Technician'")
    techs = cursor.fetchall()

    conn.close()
    return techs


# ---------- ASSIGN ----------
def assign_ticket(ticket_id, technician_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET assigned_to=?, status='Assigned'
        WHERE ticket_id=?
    """, (technician_id, ticket_id))

    conn.commit()
    conn.close()


# ---------- UPDATE STATUS ----------
def update_ticket_status(ticket_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status=?
        WHERE ticket_id=?
    """, (status, ticket_id))

    conn.commit()
    conn.close()