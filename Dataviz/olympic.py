import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
import time
from vega_datasets import data
from streamlit_vega_lite import vega_lite_component, altair_component
import pycountry as pc
import pycountry_convert as p


st.write("# Olympic Data Analysis by Team Amazeballs")

st.write("## Load data")
@st.cache(allow_output_mutation=True)
def LoadData_Countries():
    return pd.read_csv("/Users/jpgan/Documents/Code/Dataviz/countries_cleaned (1).csv")

@st.cache(allow_output_mutation=True)
def LoadData_Athletes():
    return pd.read_csv("/Users/jpgan/Documents/Code/Dataviz/athletes_cleaned (1).csv")

df_countries = LoadData_Countries()
df_athletes = LoadData_Athletes()

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
   
df_countries['alpha2'] = [p.country_name_to_country_alpha2(df_countries['Country'].iloc[i]) for i in range(len(df_countries))]
for i in range(len(df_countries)):
    if df_countries.iloc[i]['alpha2'] == 'TL':
        df_countries['alpha2'].iloc[i] = 'ID' 

df_countries['Continent'] = [p.country_alpha2_to_continent_code(df_countries['alpha2'].iloc[i]) for i in range(len(df_countries))]

st.write("### Olympic data by country:")
st.write(df_countries.head())
st.write("### Olympic data by athletes:")
st.write(df_athletes.head())

@st.cache(allow_output_mutation=True)
def plotScatterPlot():
    chart = alt.Chart(df_countries, autosize='pad').mark_circle().encode(
        x=alt.X('Medal', scale=alt.Scale(0,58)),
        y='Population',
        color='Continent',
    ).interactive()

    return chart

st.write("## Average medals per Olympics by Population")
st.altair_chart(plotScatterPlot(), use_container_width=False)
