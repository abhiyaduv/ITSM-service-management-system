from database import get_connection


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # ---------------- TICKETS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        category TEXT,
        priority TEXT,
        status TEXT,
        created_date TEXT,
        assigned_to INTEGER,
        sla_deadline TEXT
    )
    """)

 # ---------------- ASSETS TABLE ----------------
    # ---------------- ASSETS TABLE ----------------    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets(
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_name TEXT,
    asset_type TEXT,
    status TEXT,
    assigned_to INTEGER,
    purchase_date TEXT
)
""")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()