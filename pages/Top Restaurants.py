import streamlit as st
import numpy as np
import pandas as pd
from utils.CRUD import *
from utils.analys import list_to_numpy_array

@st.cache
def load_data():
    connection = connect()
    city = get_cities(connection)
    return city



city_names = load_data()
city_names = list_to_numpy_array(city_names)
city = st.selectbox("select the city", city_names)
connection = connect()
top_rests = read_top_ranks(connection, {'City': city})
print(top_rests)
top_rests = np.array(top_rests)
st.write(top_rests)




