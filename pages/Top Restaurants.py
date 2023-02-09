import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.CRUD import *
from utils.analys import list_to_numpy_array

@st.cache
def load_data():
    connection = connect()
    city = get_cities(connection)
    return city



city_names = load_data()
city_names = np.sort(list_to_numpy_array(city_names))
city = st.selectbox("select the city", city_names)
connection = connect()
top_rests = read_top_ranks(connection, {'City': city})
top_rests = np.array(top_rests)
# st.write(top_rests)

connection = connect()
top_rank_facilities = read_top_ranks_facilities(connection, {'City': city})
top_rank_facilities = np.array(top_rank_facilities)
# st.write(top_rank_facilities)

# fig, ax = plt.subplots()
# ax.hexbin(top_rank_facilities[:,1], top_rank_facilities[:, 2], gridsize=25)
# plt.xlabel('Restaurant Rate')
# plt.ylabel('Number of Facilities')
# st.pyplot(fig)

# fig, ax = plt.subplots()
# ax.stem(top_rank_facilities[:, 0], top_rank_facilities[:, 2])
# plt.xlabel('Restaurant Rate')
# plt.ylabel('Number of Facilities')
# st.pyplot(fig)


fig, ax = plt.subplots()
ax.scatter(top_rank_facilities[:, 1], top_rank_facilities[:, 2])

for r in top_rank_facilities:
    ax.annotate(r[0], (r[1], r[2]))

st.pyplot(fig)