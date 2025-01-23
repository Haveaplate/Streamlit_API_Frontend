import streamlit as st

# --- PAGE SETUP ---

guide_page = st.Page(
    page = "pages/guide.py",
    title = "Guide",
    icon = ":material/home:",
    default = True,
)

fbmonthly_page = st.Page(
    page = "pages/fbmonthly.py",
    title = "Facebook",
    icon = ":material/elderly:",
)

igmonthly_page = st.Page(
    page = "pages/igmonthly.py",
    title = "Instagram",
    icon = ":material/falling:",
)

#ttmonthly_page = st.Page(
#    page = "pages/ttmonthly.py",
#    title = "TikTok",
#    icon = ":material/child_care:",
#)

iggiveaway_page = st.Page(
    page = "pages/iggiveaway.py",
    title = "Giveaway",
    icon = ":material/featured_seasonal_and_gifts:",
)

scraper_page = st.Page(
    page = "pages/scraper.py",
    title = "Scraper",
    icon = ":material/preview:",
)

# --- NAVIGATION SETUP ---

pg = st.navigation(
    {
        "Help" : [guide_page],
        "Data" : [fbmonthly_page, igmonthly_page, iggiveaway_page],
        "Scraper" : [scraper_page]
    }
)

# --- SHARED ON ALL PAGES ---

st.logo("assets/images.png")
st.sidebar.text("Made by Jerome 🤕")

# --- RUN NAVIGATION ---

pg.run()

