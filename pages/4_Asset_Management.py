import streamlit as st
import pandas as pd
from modules.assets import (
    add_asset,
    get_assets,
    get_users,
    assign_asset,
    update_asset_status,
    delete_asset
)

# -------- LOGIN CHECK --------
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

role = st.session_state.user["role"]

if role != "Admin":
    st.error("Only Admin can manage assets ❌")
    st.stop()

st.title("🖥 Asset Management System")

# =============================
# ADD ASSET
# =============================
st.subheader("➕ Add New Asset")

asset_name = st.text_input("Asset Name")
asset_type = st.selectbox(
    "Asset Type",
    ["Laptop", "Desktop", "Server", "Printer", "Router", "Software License"]
)

if st.button("Add Asset"):

    if asset_name.strip() == "":
        st.error("Asset name required")
    else:
        add_asset(asset_name, asset_type)
        st.success("Asset Added Successfully ✅")
        st.rerun()

st.divider()

# =============================
# VIEW ASSETS
# =============================
st.subheader("📋 All Assets")

df = get_assets()

if df.empty:
    st.info("No assets available")
    st.stop()

st.dataframe(df, use_container_width=True)

st.divider()

# =============================
# ASSIGN ASSET
# =============================
st.subheader("👤 Assign Asset")

asset_ids = df["asset_id"].tolist()
selected_asset = st.selectbox("Select Asset ID", asset_ids)

users = get_users()

if users:
    user_names = [u["name"] for u in users]
    selected_user = st.selectbox("Select User", user_names)

    if st.button("Assign Asset"):
        user_id = next(u["user_id"] for u in users if u["name"] == selected_user)
        assign_asset(selected_asset, user_id)
        st.success("Asset Assigned Successfully ✅")
        st.rerun()

st.divider()

# =============================
# UPDATE STATUS
# =============================
st.subheader("🔄 Update Asset Status")

status = st.selectbox(
    "Select Status",
    ["Available", "Assigned", "Under Maintenance", "Retired"]
)

if st.button("Update Status"):
    update_asset_status(selected_asset, status)
    st.success("Status Updated ✅")
    st.rerun()

st.divider()

# =============================
# DELETE ASSET
# =============================
st.subheader("🗑 Delete Asset")

if st.button("Delete Selected Asset"):
    delete_asset(selected_asset)
    st.success("Asset Deleted Successfully ✅")
    st.rerun()