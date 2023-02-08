import streamlit as st
import numpy as np
import pandas as pd

@st.cache
def load_data(df_name):
    # df = pd.read_sql_query("SELECT * from cafe_df", conn)
    df = pd.read_csv(df_name)
    return df


facilities_df = load_data("/home/mehdi/Downloads/Telegram Desktop/facilities_df.csv")

facilities = facilities_df.columns

for f in facilities:
    st.checkbox(f)

