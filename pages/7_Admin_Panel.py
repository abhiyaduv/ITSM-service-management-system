import streamlit as st
import pandas as pd
from modules.auth import (
    register_user,
    get_all_users,
    update_user_role,
    delete_user
)
from database import get_connection

# -------- LOGIN CHECK --------
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

if st.session_state.user["role"] != "Admin":
    st.error("Access Denied ❌ (Admin Only)")
    st.stop()

st.title("👑 Admin Control Panel")

# =============================
# SYSTEM STATISTICS
# =============================
st.subheader("📊 System Overview")

conn = get_connection()

tickets = pd.read_sql_query("SELECT * FROM tickets", conn)
assets = pd.read_sql_query("SELECT * FROM assets", conn)
users = pd.read_sql_query("SELECT * FROM users", conn)

conn.close()

col1, col2, col3 = st.columns(3)
col1.metric("Total Users", len(users))
col2.metric("Total Tickets", len(tickets))
col3.metric("Total Assets", len(assets))

st.divider()

# =============================
# CREATE NEW USER
# =============================
st.subheader("➕ Create New User")

name = st.text_input("Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
role = st.selectbox("Role", ["Admin", "Technician", "Employee"])

if st.button("Create User"):

    if name and email and password:
        try:
            register_user(name, email, password, role)
            st.success("User Created Successfully ✅")
            st.rerun()
        except:
            st.error("User already exists or error occurred")
    else:
        st.warning("All fields required")

st.divider()

# =============================
# MANAGE USERS
# =============================
st.subheader("👥 Manage Users")

user_df = get_all_users()

if user_df.empty:
    st.info("No users found")
    st.stop()

st.dataframe(user_df, use_container_width=True)

user_ids = user_df["user_id"].tolist()
selected_user = st.selectbox("Select User ID", user_ids)

# Update Role
new_role = st.selectbox("Update Role", ["Admin", "Technician", "Employee"])

if st.button("Update Role"):
    update_user_role(selected_user, new_role)
    st.success("Role Updated ✅")
    st.rerun()

# Delete User
if st.button("Delete User"):
    delete_user(selected_user)
    st.success("User Deleted ✅")
    st.rerun()