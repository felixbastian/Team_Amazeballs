"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
# import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

#load data
#st.cache makes the data to be only loaded once - decorator
@st.cache
def load_data():
    athletes = pd.read_csv("data/athletes_cleaned.csv" )
    countries = pd.read_csv("data/countries_cleaned.csv" )

    return athletes, countries

# STREAMLIT APP LAYOUT
df_athletes,df_countries = load_data()

#query data
dff = []

df_countries = df_countries.sort_values(by=['Medals'], ascending = False)

for x in range(len(df_countries['Nation'])):
    nation = df_countries['Nation'].iloc[x]
    medals = [df_countries['Bronzes'].iloc[x], df_countries['Silver'].iloc[x], df_countries['Gold'].iloc[x]]
    medal = ['Bronze', 'Silver', 'Gold']
    count = df_countries['Medals'].iloc[x]

    for y in range(3):

      dff.append([nation,medals[y],medal[y],count ])

MedalDF = pd.DataFrame(dff)
MedalDF = MedalDF.rename(columns={0: "Country", 1: "Amount", 2:'Medal',3:'Sum'})
print(MedalDF.head())


st.title("Olympics dataset: An insight into countries and athletes")
st.markdown("Welcome to this in-depth introduction to [...].")

#create bar chart
def draw_bars(scope):

    # normalized
    bars = alt.Chart(MedalDF).mark_bar().encode(
        x=alt.X('Amount', stack="normalize"),
        y='Country',
        color='Medal'
    )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='Sum'
    )

    (bars + text).properties()

    return (bars + text).properties()


#display bar chart
#st.write(draw_bars(['Total']))


#Radiobuttons to select

barSelection = st.radio(
     "Select the scope",
     ('Total', 'Medals/GDP', 'Medals/Population'))

st.write(draw_bars(barSelection))

# if genre == 'Comedy':
#      st.write('You selected comedy.')





# Box to select
# option = st.selectbox(
#      'How would you like to be contacted?',
#      ('Email', 'Home phone', 'Mobile phone'))
#
# st.write('You selected:', option)


# # FUNCTION FOR AIRPORT MAPS
# def map(data, lat, lon, zoom):
#     st.write(
#         pdk.Deck(
#             map_style="mapbox://styles/mapbox/light-v9",
#             initial_view_state={
#                 "latitude": lat,
#                 "longitude": lon,
#                 "zoom": zoom,
#                 "pitch": 50,
#             },
#             layers=[
#                 pdk.Layer(
#                     "HexagonLayer",
#                     data=data,
#                     get_position=["lon", "lat"],
#                     radius=100,
#                     elevation_scale=4,
#                     elevation_range=[0, 1000],
#                     pickable=True,
#                     extruded=True,
#                 ),
#             ],
#         )
#     )
#
#
# # FILTER DATA FOR A SPECIFIC HOUR, CACHE
# @st.experimental_memo
# def filterdata(df, hour_selected):
#     return df[df["date/time"].dt.hour == hour_selected]
#
#
# # CALCULATE MIDPOINT FOR GIVEN SET OF DATA
# @st.experimental_memo
# def mpoint(lat, lon):
#     return (np.average(lat), np.average(lon))
#
#
# # FILTER DATA BY HOUR
# @st.experimental_memo
# def histdata(df, hr):
#     filtered = data[
#         (df["date/time"].dt.hour >= hr) & (df["date/time"].dt.hour < (hr + 1))
#     ]
#
#     hist = np.histogram(filtered["date/time"].dt.minute, bins=60, range=(0, 60))[0]
#
#     return pd.DataFrame({"minute": range(60), "pickups": hist})
#
#
# # STREAMLIT APP LAYOUT
# data = load_data()
#
# # LAYING OUT THE TOP SECTION OF THE APP
# row1_1, row1_2 = st.columns((2, 3))
#
# with row1_1:
#     st.title("NYC Uber Ridesharing Data")
#     hour_selected = st.slider("Select hour of pickup", 0, 23)
#
# with row1_2:
#     st.write(
#         """
#     ##
#     Examining how Uber pickups vary over time in New York City's and at its major regional airports.
#     By sliding the slider on the left you can view different slices of time and explore different transportation trends.
#     """
#     )
#
# # LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
# row2_1, row2_2, row2_3, row2_4 = st.columns((2, 1, 1, 1))
#
# # SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
# la_guardia = [40.7900, -73.8700]
# jfk = [40.6650, -73.7821]
# newark = [40.7090, -74.1805]
# zoom_level = 12
# midpoint = mpoint(data["lat"], data["lon"])
#
# with row2_1:
#     st.write(
#         f"""**All New York City from {hour_selected}:00 and {(hour_selected + 1) % 24}:00**"""
#     )
#     map(filterdata(data, hour_selected), midpoint[0], midpoint[1], 11)
#
# with row2_2:
#     st.write("**La Guardia Airport**")
#     map(filterdata(data, hour_selected), la_guardia[0], la_guardia[1], zoom_level)
#
# with row2_3:
#     st.write("**JFK Airport**")
#     map(filterdata(data, hour_selected), jfk[0], jfk[1], zoom_level)
#
# with row2_4:
#     st.write("**Newark Airport**")
#     map(filterdata(data, hour_selected), newark[0], newark[1], zoom_level)
#
# # CALCULATING DATA FOR THE HISTOGRAM
# chart_data = histdata(data, hour_selected)
#
# # LAYING OUT THE HISTOGRAM SECTION
# st.write(
#     f"""**Breakdown of rides per minute between {hour_selected}:00 and {(hour_selected + 1) % 24}:00**"""
# )
#
# st.altair_chart(
#     alt.Chart(chart_data)
#     .mark_area(
#         interpolate="step-after",
#     )
#     .encode(
#         x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
#         y=alt.Y("pickups:Q"),
#         tooltip=["minute", "pickups"],
#     )
#     .configure_mark(opacity=0.2, color="red"),
#     use_container_width=True,
# )