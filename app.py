import streamlit as st
from modules.auth import login_user, register_user
from init_db import init_database

# ---------------- APP CONFIG ----------------
st.set_page_config(
    page_title="ITSM Service Management System",
    page_icon="💻",
    layout="wide"
)

# ---------------- INIT DATABASE ----------------
init_database()

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

st.title("💻 IT Infrastructure Service Management System")

# =====================================================
# USER LOGGED IN
# =====================================================
if st.session_state.user:

    user = st.session_state.user
    role = user["role"]

    st.sidebar.success(f"Logged in as {user['name']} ({role})")

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.sidebar.markdown("## Navigation")

    # ================= ADMIN =================
    if role == "Admin":

        st.sidebar.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
        st.sidebar.page_link("pages/2_Raise_Ticket.py", label="🎫 Raise Ticket")
        st.sidebar.page_link("pages/3_Manage_Tickets.py", label="🛠 Manage Tickets")
        st.sidebar.page_link("pages/4_Asset_Management.py", label="🖥 Asset Management")
        st.sidebar.page_link("pages/7_Admin_Panel.py", label="👑 Admin Panel")

    # ================= TECHNICIAN =================
    elif role == "Technician":

        st.sidebar.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
        st.sidebar.page_link("pages/3_Manage_Tickets.py", label="🛠 Manage Tickets")

    # ================= EMPLOYEE =================
    elif role == "Employee":

        st.sidebar.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
        st.sidebar.page_link("pages/2_Raise_Ticket.py", label="🎫 Raise Ticket")

    st.info("Select a page from the sidebar.")

# =====================================================
# USER NOT LOGGED IN
# =====================================================
else:

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Navigation", menu)

    # ---------------- LOGIN ----------------
    if choice == "Login":

        st.subheader("🔐 User Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if email and password:
                user = login_user(email, password)

                if user:
                    st.session_state.user = dict(user)
                    st.success("Login Successful ✅")
                    st.rerun()
                else:
                    st.error("Invalid Credentials ❌")
            else:
                st.warning("Enter all fields")

    # ---------------- REGISTER ----------------
    elif choice == "Register":

        st.subheader("📝 Create Account")

        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

       
        role = st.selectbox(
    "Role",
    ["Admin", "Employee", "Technician"]
)
        if st.button("Register"):

            if name and email and password:
                try:
                    register_user(name, email, password, role)
                    st.success("Account Created Successfully ✅")
                except:
                    st.error("User already exists")
            else:
                st.warning("All fields required")