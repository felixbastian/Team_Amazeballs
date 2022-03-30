import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
import time
from vega_datasets import data
from streamlit_vega_lite import vega_lite_component, altair_component
import pycountry as pc
import pycountry_convert as p
import numpy as np


def app():

    @st.cache(allow_output_mutation=True)
    def LoadData_Countries():
        return pd.read_csv("data/countries_cleaned.csv")

    @st.cache(allow_output_mutation=True)
    def LoadData_Athletes():
        return pd.read_csv("data/athletes_cleaned.csv")

    df_countries = LoadData_Countries()
    df_athletes = LoadData_Athletes()

    # Last minute data cleaning

    # Taking out sports with nearly no medal information
    df_athletes = df_athletes[df_athletes['Sport'] != str('Aeronautics')]
    df_athletes = df_athletes[df_athletes['Sport'] != str('Alpinism')]
    df_athletes = df_athletes[df_athletes['Sport'] != str('Basque Pelota')]
    df_athletes = df_athletes[df_athletes['Sport'] != str('Military Ski Patrol')]

    df_countries = df_countries.rename({'Medal': 'Average Medals', 'Medal.1': 'Total Medals', 'Medals': 'Medals in Best Sport',
                                        'MostSuccessfulSport': 'Most Successful Sport'}, axis="columns")
    df_countries.head()
    df_athletes.head()

    df_countries['Country'] = ""
    for i in range(len(df_countries)):
        if df_countries.iloc[i]['Nation'] == 'Chinese Taipei':
            df_countries['Country'].iloc[i] = 'Taiwan'
        elif df_countries.iloc[i]['Nation'] == 'DR Congo':
            df_countries['Country'].iloc[i] = 'Congo'
        elif df_countries.iloc[i]['Nation'] == 'Korea, North':
            df_countries['Country'].iloc[i] = 'North Korea'
        elif df_countries.iloc[i]['Nation'] == 'Korea, South':
            df_countries['Country'].iloc[i] = 'South Korea'
        elif df_countries.iloc[i]['Nation'] == 'Kosovo':
            df_countries['Country'].iloc[i] = 'Serbia'
        elif df_countries.iloc[i]['Nation'] == 'Serbia and Montenegro':
            df_countries['Country'].iloc[i] = 'Montenegro'
        elif df_countries.iloc[i]['Nation'] == 'Sudan, South':
            df_countries['Country'].iloc[i] = 'Sudan'
        elif df_countries.iloc[i]['Nation'] == 'The Gambia':
            df_countries['Country'].iloc[i] = 'Gambia'
        elif df_countries.iloc[i]['Nation'] == 'Virgin Islands':
            df_countries['Country'].iloc[i] = 'British Virgin Islands'
        else:
            df_countries['Country'].iloc[i] = df_countries['Nation'].iloc[i]

    df_countries['alpha2'] = [p.country_name_to_country_alpha2(
        df_countries['Country'].iloc[i]) for i in range(len(df_countries))]
    for i in range(len(df_countries)):
        if df_countries.iloc[i]['alpha2'] == 'TL':
            df_countries['alpha2'].iloc[i] = 'ID'

    df_countries['Continent'] = [p.country_alpha2_to_continent_code(
        df_countries['alpha2'].iloc[i]) for i in range(len(df_countries))]

    @st.cache(allow_output_mutation=True)
    def plotScatterPlot():
        input_dropdown = alt.binding_select(
            options=df_countries['Continent'].unique().tolist(), name='Continent')
        selection = alt.selection_single(fields=['Continent'], bind=input_dropdown, clear=True)

        chart = alt.Chart(df_countries, autosize='pad').mark_circle().encode(
            y=alt.Y('Total Medals', scale=alt.Scale(zero=True)),
            x=alt.X('Apps', scale=alt.Scale(zero=False)),
            color='Continent',
            size=alt.Size('Population', scale=alt.Scale(
                domain=[0.125, 1500000000], range=[200, 4000])),
            tooltip=['Nation', 'Apps', 'First_App', 'Total Medals', 'Average Medals', 'Most Successful Sport',
                     'Medals in Best Sport', 'Population'],
        ).configure_view(continuousWidth=1000,
                         continuousHeight=500).configure_circle(size=400, opacity=0.5
                                                                ).add_selection(selection).transform_filter(selection).interactive()

        return chart

    st.write("## No. of Olympic Apps vs. Total Medals Won")
    st.write("This graph allows the user to visualize how talented each country is at the Olympics, relative to its number of appearances at the Olympics and its population. With this, we are able to spot countries (and even continents) who underperform despite its population or despite its longevity in the games, and vice versa. The graph is interactive, feel free to pan, zoom in, zoom out, and filter by continent to analyze with more depth. Hover over each mark to get more information about each country. To reset the graph or to remove filters, just double click anywhere on it.")
    st.altair_chart(plotScatterPlot(), use_container_width=False)
