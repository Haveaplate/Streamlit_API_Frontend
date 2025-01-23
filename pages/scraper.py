import streamlit as st
from functions.functions_scraper import scrape_website, extract_body_content, clean_body_content, split_dom_content, parse_with_ollama

st.title("Scraper")

st.write("*does not work for social media yet cause of login prompt* 💀")

url = st.text_input("Enter the Website URL")

if st.button("Scrape Site"):
    st.write("Scraping the website...")

    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

if "dom_content" in st.session_state:
    with st.expander("View Content"):
        st.text_area("Content", st.session_state.dom_content, height = 300)

    parse_description = st.text_area("describe what you want...")

    if st.button("Generate"):
        if parse_description:
            st.write("Generating the content...")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)

            st.write(result)

