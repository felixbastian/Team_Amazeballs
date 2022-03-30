#app.pyimport app1
import olympic
import Data_overview
import sports_view
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

PAGES = {
    "Data overview": Data_overview,
    "Olympic success": olympic,
    "Olympic sports overview": sports_view
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()