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

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

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
df_countries = df_countries.rename({'Medal':'Average Medals','Medal.1': 'Total Medals'
,'Medals': 'Medals in Best Sport',
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
    input_dropdown = alt.binding_select(options=df_countries['Continent'].unique().tolist()
    , name='Continent')
    selection = alt.selection_single(fields=['Continent'], bind=input_dropdown, clear=True)
    
    chart = alt.Chart(df_countries, autosize='pad').mark_circle().encode(
        y=alt.Y('Total Medals', scale=alt.Scale(zero=True)),
        x=alt.X('Apps', scale=alt.Scale(zero=False)),
        color='Continent',
        size = alt.Size('Population', scale = alt.Scale(domain = [0.125,1500000000], range=[200,4000])),
        tooltip = ['Nation', 'Apps', 'First_App', 'Total Medals', 'Average Medals', 'Most Successful Sport', 
        'Medals in Best Sport', 'Population'],
    ).configure_view(continuousWidth=1000, 
    continuousHeight=500).configure_circle(size=400, opacity=0.5
    ).add_selection(selection).transform_filter(selection).interactive()

    return chart

st.write("## No. of Olympic Apps vs. Total Medals Won")
st.write("This graph allows the user to visualize how good each country is at the Olympics, relative to its number of appearances at the Olympics and its population. With this, we are able to spot countries (and even continents) who underperform despite its population or despite its longevity in the games, and vice versa. The graph is interactive, feel free to pan, zoom in, zoom out, and filter by continent to analyze with more depth. Hover over each mark to get more information about each country. To reset the graph or to remove filters, just double click anywhere on it.")
st.altair_chart(plotScatterPlot(), use_container_width=False)

dff = []
df_countries = df_countries.sort_values(by=['Total Medals'], ascending = False)

for x in range(len(df_countries['Nation'])):
    nation = df_countries['Nation'].iloc[x]
    medals = [df_countries['Bronze'].iloc[x], df_countries['Silver'].iloc[x], df_countries['Gold'].iloc[x]]
    medal = ['Bronze', 'Silver', 'Gold']
    ordering = [1,2,3]
    count = df_countries['Total Medals'].iloc[x]

    for y in range(3):


      dff.append([nation,medals[y],medal[y],count ,ordering[y]])

MedalDF = pd.DataFrame(dff)
MedalDF = MedalDF.rename(columns={0: "Country", 1: "Amount", 2:'Medal',3:'Sum',4:'Ordering'})
sort = MedalDF.sort_values('Sum', ascending=False)
sortOrderAll = sort['Country'].unique()

print(MedalDF.head())


#Althetes DF
sportSet = sorted(set(df_athletes['Sport'].unique()))
sportSet.insert(0,'All')

def createAthletesDF(scope):
    # Filter DF by sport and teams that won a medal to reduce amount of data
    filter = df_athletes[df_athletes['Sport'] == str(scope)]
    filter = filter[filter['Medal'].notnull()]

    # if team sport, only take one medal for entire team
    uniqueSports = df_athletes['Sport'].unique().tolist()
    isTeamSport = [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                   0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]
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

        countryFilter = filter[filter['Team']==str(participant)].drop_duplicates()
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
    AthletesDF = AthletesDF.rename(columns={0: "Country", 1: "Amount", 2: 'Medal', 3: 'Sum', 4: 'Ordering'})
    sort = AthletesDF.sort_values('Sum', ascending=False)
    sortOrder = sort['Country'].unique()

    return AthletesDF, sortOrder


#create bar chart
def draw_bars(scope):

    #initialization parameter
    data = MedalDF
    sortOrder = sortOrderAll

    #the All data comes from the countries database and the specific sport
    #from the sports database that needs filtering by sport first of course
    # -> createAthletesDF
    if(scope == 'All'): data = MedalDF
    else:
        data,sortOrder = createAthletesDF(scope)

    #define number of data points to show
    data = data.sort_values('Sum', ascending=False)
    data = data.iloc[0:30,:]


    base = alt.Chart(data).encode(
        x=alt.X('Amount', stack="normalize"),
        #y=alt.Y('Country', sort=alt.EncodingSortField(field="Country", op="count", order='descending')),
        y=alt.Y('Country', sort=sortOrder)

    )

    bars = base.mark_bar().encode(
        color=alt.Color('Medal',  sort=alt.EncodingSortField('Ordering', order='ascending')),
        order='Ordering'
        )

    text = base.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='Sum'
    )


    return (bars + text).properties()

#Box to select

st.markdown("## Breakdown of Medals Won by Country and Sport")
option = st.selectbox(
     'Select the sport',
     (sportSet))

st.write(draw_bars(option))
