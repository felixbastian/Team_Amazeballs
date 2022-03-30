import streamlit as st
import pandas as pd
import altair as alt
import pycountry_convert as p


def app():

    st.title("Olympics dataset: An insight into countries and athletes")

    st.write("## Load data")

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

    st.write("### Olympic data by country:")
    st.write(df_countries.head())
    st.write("### Olympic data by athletes:")
    st.write(df_athletes.head())
