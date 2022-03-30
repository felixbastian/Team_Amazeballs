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

    dff = []
    df_countries = df_countries.sort_values(by=['Total Medals'], ascending=False)

    for x in range(len(df_countries['Nation'])):
        nation = df_countries['Nation'].iloc[x]
        medals = [df_countries['Bronze'].iloc[x],
                  df_countries['Silver'].iloc[x], df_countries['Gold'].iloc[x]]
        medal = ['Bronze', 'Silver', 'Gold']
        ordering = [1, 2, 3]
        count = df_countries['Total Medals'].iloc[x]

        for y in range(3):

            dff.append([nation, medals[y], medal[y], count, ordering[y]])

    MedalDF = pd.DataFrame(dff)
    MedalDF = MedalDF.rename(columns={0: "Country", 1: "Amount",
                                      2: 'Medal', 3: 'Sum', 4: 'Ordering'})
    sort = MedalDF.sort_values('Sum', ascending=False)
    sortOrderAll = sort['Country'].unique()

    print(MedalDF.head())

    # Althetes DF
    sportSet = sorted(set(df_athletes['Sport'].unique()))
    sportSet.insert(0, 'All')

    def createAthletesDF(scope):
        # Filter DF by sport and teams that won a medal to reduce amount of data
        filter = df_athletes[df_athletes['Sport'] == str(scope)]
        filter = filter[filter['Medal'].notnull()]

        # if team sport, only take one medal for entire team
        uniqueSports = df_athletes['Sport'].unique().tolist()
        isTeamSport = [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1,
                       0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1]
        sportIndex = uniqueSports.index(str(scope))
        isTeam = isTeamSport[sportIndex]

        # filter by year if teamsports is 1
        if (isTeam == 1):
            # takes out all columns to prepare for dublicate reduction
            filter = filter.iloc[:, 6:]

        participants = filter['Team'].unique()

        liste = []

        # iterate through all participating countries and filter medals out
        for participant in participants:
            Bronze = 0
            Silver = 0
            Gold = 0

            countryFilter = filter[filter['Team'] == str(participant)].drop_duplicates()
            Gold = len(countryFilter[countryFilter['Medal'] == 'Gold'])
            Silver = len(countryFilter[countryFilter['Medal'] == 'Silver'])
            Bronze = len(countryFilter[countryFilter['Medal'] == 'Bronze'])
            Sum = Gold + Silver + Bronze

            BronzeRow = [participant, Bronze, 'Bronze', Sum, 1]
            SilverRow = [participant, Silver, 'Silver', Sum, 2]
            GoldRow = [participant, Gold, 'Gold', Sum, 3]

            liste.append(BronzeRow)
            liste.append(SilverRow)
            liste.append(GoldRow)

        AthletesDF = pd.DataFrame(liste)
        AthletesDF = AthletesDF.rename(
            columns={0: "Country", 1: "Amount", 2: 'Medal', 3: 'Sum', 4: 'Ordering'})
        sort = AthletesDF.sort_values('Sum', ascending=False)
        sortOrder = sort['Country'].unique()

        return AthletesDF, sortOrder

    # create bar chart

    def draw_bars(scope):

        # initialization parameter
        data = MedalDF
        sortOrder = sortOrderAll

        # the All data comes from the countries database and the specific sport
        # from the sports database that needs filtering by sport first of course
        # -> createAthletesDF
        if(scope == 'All'):
            data = MedalDF
        else:
            data, sortOrder = createAthletesDF(scope)

        # define number of data points to show
        data = data.sort_values('Sum', ascending=False)
        data = data.iloc[0:60, :]

        base = alt.Chart(data).encode(
            #x=alt.X('Amount', stack="normalize"),
            x=alt.X('Amount'),
            #y=alt.Y('Country', sort=alt.EncodingSortField(field="Country", op="count", order='descending')),
            y=alt.Y('Country', sort=sortOrder)

        )

        bars = base.mark_bar().encode(
            #color=alt.Color('Medal', sort=alt.EncodingSortField('Ordering', order='ascending') ),
            color=alt.Color('Medal', sort=alt.EncodingSortField('Ordering', order='ascending'),
                            legend=alt.Legend(
                                legendX=130, legendY=-40, orient='top', direction='horizontal', titleAnchor='middle'),
                            scale=alt.Scale(
                                domain=['Bronze', 'Silver', 'Gold'],
                                range=['brown', 'silver', 'gold'])),
            order='Ordering'
        )

        # text = base.mark_text(
        #     align='left',
        #     baseline='middle',
        #     dx=3  # Nudges text to right so it doesn't appear on top of the bar
        # ).encode(
        #     text='Sum'
        # )

        return bars

    # Box to select
    # filterSet = ['All']

    st.markdown("## Breakdown of Medals Won by Country and Sport")

    option = st.selectbox('Select the sport', (sportSet))

    # change(sportSet,0)
    st.write(draw_bars(option))

    # Radiobuttons to select

    # radioSelection = st.radio(
    #      "Select the scope",
    #      ('By Country', 'By Sport'))

    #
    # #st.write(draw_bars(radioSelection))
    #
    # if radioSelection == 'By Sport':
    #
    #      overallScope = 'Country'
    #      filterSet = ['All', 'Ho']
    #      st.write(draw_bars(change(filterSet, 1)))
    #
    #
    #
    # elif radioSelection == 'By Country':
    #      overallScope = 'Sport'
    #
    #      st.write(draw_bars(change(sportSet, 1)))
