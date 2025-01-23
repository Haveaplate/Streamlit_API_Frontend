import streamlit as st
from functions.functions_data import is_valid_date, is_fully_numeric, get_insta_page_data

st.title("Instagram")

col1, col2 = st.columns(2, gap = "small", vertical_alignment = "center")

with col1:
    accid = st.text_input("Account ID")
    date = st.text_input("Date (YYYY-MM)")

with col2:
    accname = st.text_input("Account Name")
    user_token = st.text_input("User Access Token")

submit_button = st.button("Get Data")

if submit_button:
    if not accid:
        st.error("Please provide the account ID...")
        st.stop()

    if not is_fully_numeric(accid):
        st.error("Please provide a valid account ID...")
        st.stop()

    if not accname:
        st.error("Please provide the account name...")
        st.stop()

    if not is_valid_date(date):
        st.error("Please provide a valid date...")
        st.stop()

    if not user_token:
        st.error("Please provide a access token...")
        st.stop()

    try:
        csv_data = get_insta_page_data(accid, date, user_token)
        st.success("Data fetched successfully!")

        csv_data.seek(0)
        st.download_button(label = "Download CSV", data = csv_data.getvalue(), file_name = f"{accname}_{date}_IG.csv")

    except Exception as e:
        st.error(f"Error: {e}")

