import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
from vega_datasets import data
from streamlit_vega_lite import vega_lite_component, altair_component
import time

def app():
    
    st.write('# Characteristics of champions')

    @st.cache
    def loadData():
        return pd.read_csv('data/df_characteristics.csv')

    df_char = loadData()
    data = df_char

    st.markdown("## Age distribution")

    TeamSet = list(data['Team'].unique())
    TeamSet.sort()

    selection = alt.selection_single(fields=['Team'], bind=alt.binding_select(options=TeamSet) , name = 'Select')

    chart = alt.Chart(data).mark_circle().add_selection(
        selection
    ).encode(
        x="Sex:O",
        y="Age:Q",
        tooltip="Age:Q",
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.05))
    )

    st.write(chart)

########################################################


    st.markdown("## Height distribution")

    TeamSet = list(data['Team'].unique())
    TeamSet.sort()

    selection = alt.selection_single(fields=['Team'], bind=alt.binding_select(options=TeamSet) , name = 'Select')

    chart = alt.Chart(data).mark_circle().add_selection(
        selection
    ).encode(
        x="Sex:O",
        y="Height:Q",
        tooltip="Height:Q",
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.05))
    )

    st.write(chart)

##########################################################


    st.markdown("## Weight distribution")

    TeamSet = list(data['Team'].unique())
    TeamSet.sort()

    selection = alt.selection_single(fields=['Team'], bind=alt.binding_select(options=TeamSet) , name = 'Select')

    chart = alt.Chart(data).mark_circle().add_selection(
        selection
    ).encode(
        x="Sex:O",
        y="Weight:Q",
        tooltip="Weight:Q",
        opacity=alt.condition(selection, alt.value(0.75), alt.value(0.05))
    )

    st.write(chart)
