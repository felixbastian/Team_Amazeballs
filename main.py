#app.pyimport app1
import olympic
import Data_overview
import sports_view
import gender_contribution
import characteristics
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

PAGES = {
    "Data overview": Data_overview,
    "Olympic success": olympic,
    "Olympic sports overview": sports_view,
    "Gender based medal distribution": gender_contribution,
    "Athlete characteristics": characteristics
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
