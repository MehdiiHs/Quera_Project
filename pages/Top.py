import streamlit as st
import pandas as pd
from utils.analys import *
import altair as alt
import folium

@st.cache
def load_data(df_name):
    # df = pd.read_sql_query("SELECT * from cafe_df", conn)
    df = pd.read_csv(df_name)
    return df

df = load_data("/home/mehdi/Downloads/Telegram Desktop/cafe_df.csv")
location_df = load_data("/home/mehdi/Downloads/Telegram Desktop/location_df.csv")

city_names = get_cities(location_df)

city = st.selectbox("select the city", city_names)
st.write(location_df[location_df.City == city])




