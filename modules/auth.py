from database import get_connection
import bcrypt
import pandas as pd


# ---------------- HASH PASSWORD ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)


# ---------------- REGISTER ----------------
def register_user(name, email, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(password)

    cursor.execute("""
        INSERT INTO users(name,email,password,role)
        VALUES(?,?,?,?)
    """, (name, email, hashed, role))

    conn.commit()
    conn.close()


# ---------------- LOGIN ----------------
def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user and check_password(password, user["password"]):
        return user

    return None


# ---------------- GET ALL USERS ----------------
def get_all_users():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT user_id, name, email, role
        FROM users
        ORDER BY user_id DESC
    """, conn)

    conn.close()
    return df


# ---------------- UPDATE ROLE ----------------
def update_user_role(user_id, role):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET role=?
        WHERE user_id=?
    """, (role, user_id))

    conn.commit()
    conn.close()


# ---------------- DELETE USER ----------------
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()