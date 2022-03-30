import streamlit as st
import pandas as pd
import altair as alt
from altair import datum
from vega_datasets import data
from streamlit_vega_lite import vega_lite_component, altair_component
import time

def app():
    st.write('# Summer Games')

    @st.cache
    def loadData():
        return pd.read_csv('data/df_summer.csv')

    df_map_summer = loadData()


    sportSet = sorted(set(df_map_summer['Sport'].unique()))

    def createAthletesDF(scope):
        # Filter DF by sport and teams that won a medal to reduce amount of data
        filter = df_map_summer[df_map_summer['Sport'] == str(scope)]
        participants = filter['Team'].unique()
        years = filter['Year'].unique()


        liste = []

        # iterate through all participating countries and filter genders out
        for participant in participants:
            for year in years: 
                Male = 0
                Female = 0
                countryFilter = filter[filter['Team'] == str(participant)]
                yearFilter = countryFilter[countryFilter['Year'] == year]
                Male = len(yearFilter[yearFilter['Sex']=='M'])
                Female = len(yearFilter[yearFilter['Sex']=='F'])
                Sum = Male + Female

                MaleRow = [participant, year, Male, 'Male', Sum, 1]
                FemaleRow = [participant, year, Female, 'Female', Sum, 2]

                liste.append(MaleRow)
                liste.append(FemaleRow)

        AthletesDF = pd.DataFrame(liste)
        AthletesDF = AthletesDF.rename(columns={0: "Country", 1: "Year", 2: "Amount", 3: 'Gender', 4: 'Sum', 5: 'Ordering'})
        sort = AthletesDF.sort_values('Sum', ascending=False)
        sortOrder = sort['Country'].unique()

        return AthletesDF, sortOrder


    st.markdown("## Breakdown of Medals Won by Genders in Country and Sport")

    option = st.selectbox('Select the sport',(sportSet))


    data,sortOrder = createAthletesDF(option)

    date_slider = alt.binding_range(min=min(data['Year']), max=max(data['Year']), step=4)
    slider_selection = alt.selection_single(bind=date_slider, fields=['Year'], name = 'Slider', init={'Year': 1896})


    bars = alt.Chart(data).mark_bar().encode(
        x=alt.X('Amount:O', stack='zero'),
        y=alt.Y('Country:N', sort = sortOrder),
        color=alt.Color('Gender:N')
    ).add_selection(slider_selection).transform_filter(slider_selection)

    text = alt.Chart(data).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('Amount:O', stack='zero'),
        y=alt.Y('Country:N'),
        detail='Gender:N'
    )

    st.write(bars + text)

#####################################################################################################################################

    st.write('# Winter Games')
    @st.cache
    def loadData():
        return pd.read_csv('data/df_winter.csv')

    df_map_winter = loadData()


    sportSet = sorted(set(df_map_winter['Sport'].unique()))

    def createAthletesDF(scope):
        # Filter DF by sport and teams that won a medal to reduce amount of data
        filter = df_map_winter[df_map_winter['Sport'] == str(scope)]
        participants = filter['Team'].unique()
        years = filter['Year'].unique()


        liste = []

        # iterate through all participating countries and filter genders out
        for participant in participants:
            for year in years: 
                Male = 0
                Female = 0
                countryFilter = filter[filter['Team'] == str(participant)]
                yearFilter = countryFilter[countryFilter['Year'] == year]
                Male = len(yearFilter[yearFilter['Sex']=='M'])
                Female = len(yearFilter[yearFilter['Sex']=='F'])
                Sum = Male + Female

                MaleRow = [participant, year, Male, 'Male', Sum, 1]
                FemaleRow = [participant, year, Female, 'Female', Sum, 2]

                liste.append(MaleRow)
                liste.append(FemaleRow)

        AthletesDF = pd.DataFrame(liste)
        AthletesDF = AthletesDF.rename(columns={0: "Country", 1: "Year", 2: "Amount", 3: 'Gender', 4: 'Sum', 5: 'Ordering'})
        sort = AthletesDF.sort_values('Sum', ascending=False)
        sortOrder = sort['Country'].unique()

        return AthletesDF, sortOrder


    st.markdown("## Breakdown of Medals Won by Genders in Country and Sport")

    option = st.selectbox('Select the sport',(sportSet))


    data,sortOrder = createAthletesDF(option)

    date_slider = alt.binding_range(min=min(data['Year']), max=max(data['Year']), step=4)
    slider_selection = alt.selection_single(bind=date_slider, fields=['Year'], name = 'Slider', init={'Year': 1924})


    bars = alt.Chart(data).mark_bar().encode(
        x=alt.X('Amount:O', stack='zero'),
        y=alt.Y('Country:N', sort = sortOrder),
        color=alt.Color('Gender:N')
    ).add_selection(slider_selection).transform_filter(slider_selection)

    text = alt.Chart(data).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('Amount:O', stack='zero'),
        y=alt.Y('Country:N'),
        detail='Gender:N'
    )

    st.write(bars + text)
