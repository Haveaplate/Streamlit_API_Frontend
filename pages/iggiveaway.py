import streamlit as st
from functions.functions_data import is_fully_numeric, get_insta_post

st.title("IG Giveaway")

col1, col2 = st.columns(2, gap = "small", vertical_alignment = "top")

with col1:
    postid = st.text_input("Post ID")
    user_token = st.text_input("User Access Token")

with col2:
    giveawayname = st.text_input("Giveaway Name")

submit_button = st.button("Get Data")

if submit_button:
    if not postid:
        st.error("Please provide the post ID...")
        st.stop()

    if not is_fully_numeric(postid):
        st.error("Please provide a valid post ID...")
        st.stop()

    if not giveawayname:
        st.error("Please provide the giveaway name...")
        st.stop()

    if not user_token:
        st.error("Please provide a access token...")
        st.stop()

    try:
        csv_data = get_insta_post(postid, user_token)
        st.success("Data fetched successfully!")

        csv_data.seek(0)
        st.download_button(label = "Download CSV", data = csv_data.getvalue(), file_name = f"{giveawayname}_giveaway.csv")

    except Exception as e:
        st.error(f"Error: {e}")

