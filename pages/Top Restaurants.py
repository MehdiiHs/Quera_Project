import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.CRUD import *
from utils.analys import list_to_numpy_array
from bidi.algorithm import get_display
from arabic_reshaper import reshape

@st.cache
def load_data():
    connection = connect()
    city = get_cities(connection)
    return city

city_names = load_data()
city_names = np.sort(list_to_numpy_array(city_names))
city = st.selectbox("Select the city:", city_names)


# Add a separator
st.write(30*'*')



connection = connect()
top_rests = read_top_ranks(connection, {'City': city})
top_rests = np.array(top_rests)

connection = connect()
top_rank_facilities = read_top_ranks_facilities(connection, {'City': city})
top_rank_facilities = np.array(top_rank_facilities)

connection = connect()
best_facilities, facilities = read_best_facilities(connection,  {'City': city})
best_facilities = list_to_numpy_array(best_facilities)
facilities = [get_display(reshape(f)) for f in facilities]


# Add a subheader
st.subheader('Number of Facilities for Top 50 Restaurants')

# Create the bar chart and add labels, title and grid lines
fig1, ax1 = plt.subplots(figsize=(15, 12), dpi=300,  facecolor='#0e1117')
ax1.set_facecolor(color='#0e1117')
ax1.barh(facilities, best_facilities, color='#1f77b4', edgecolor='white', linewidth=1.5)
ax1.set_xlabel('Number of Restaurants With Facility', fontsize=20, labelpad=15,color='white')
ax1.set_ylabel('Facility', fontsize=20, labelpad=15, color='white')
ax1.xaxis.set_tick_params(labelsize=20, labelcolor='white')
ax1.yaxis.set_tick_params(labelsize=20, labelcolor='white')
ax1.grid(axis='x', color='white', linestyle='-', linewidth=0.5, alpha=0.5)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)
st.pyplot(fig1)

connection = connect()
most_restaurants = read_cities_with_most_top_restaurants(connection)
most_restaurants = np.array(most_restaurants)
most_restaurants[:, 0] = [get_display(reshape(f)) for f in most_restaurants[:, 0]]


# Add a separator
st.write(30*'*')


# Add a subheader
st.subheader('Cities with the Most Top 50 Restaurants')

# Create the pie chart and rotate the percentage labels
fig2, ax2 = plt.subplots(figsize=(15, 8), dpi=300)
fig2.set_facecolor('#0e1117')
wedges, texts, autotexts = ax2.pie(most_restaurants[:, 1], labels=most_restaurants[:, 0], startangle=90, autopct='%1.1f%%', rotatelabels=True)

# Set font size for the pie chart
for label, autotext in zip(texts, autotexts):
    autotext.set_rotation(label.get_rotation())
    autotext.set_fontsize(8)
    label.set_fontsize(12)
    label.set_color("white")

# Set colors for the pie chart
colors = plt.cm.rainbow(np.linspace(0, 1, len(wedges)))
for i, wedge in enumerate(wedges):
    wedge.set_facecolor(colors[i])

# Show the plot
st.pyplot(fig2)


connection = connect()
rate_on_foodtype = read_rating_variant_foodtype(connection, {'City': city})
rate_on_foodtype = np.array(rate_on_foodtype)
rate_on_foodtype[:, 0] = [get_display(reshape(f)) for f in rate_on_foodtype[:, 0]]

# Add a separator
st.write(30*'*')


# Add a subheader
st.subheader('Comparing Food Type And Rating')

fig3, ax3 = plt.subplots(figsize=(15, 12), dpi=300,  facecolor='#0e1117')
ax3.set_facecolor(color='#0e1117')
opacity = 1
bar_width = 0.35
bar1 = ax3.bar(rate_on_foodtype[:, 0], rate_on_foodtype[:, 2], align='center', alpha=opacity, color='#330066', label='food type')
bar2 = ax3.bar(rate_on_foodtype[:, 0], rate_on_foodtype[:, 1]+bar_width, bar_width, align='center', alpha=opacity, color='#ff69cb', label='rating')

ax3.xaxis.set_tick_params(labelsize=16, labelcolor='white', rotation=45)
ax3.yaxis.set_tick_params(labelsize=16, labelcolor='white')
ax3.legend(fontsize=20)
# Add counts above the two bar graphs
for rect in bar1 + bar2:
    height = rect.get_height()
    ax3.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.0f}', ha='center', va='bottom',color='white', size=12)

# Show the plot
st.pyplot(fig3)


# Add a separator
st.write(30*'*')


# Add a subheader
st.subheader('Average Working Time Based on Rating Range')
connection = connect()
avg_working_hour = read_time_average(connection,  {'City': city})

avg_working_hour = np.array(avg_working_hour)
avg_working_hour[:, 0] = [str(s) for s in avg_working_hour[:, 0]]

bar_width = 0.35
fig4, ax4 = plt.subplots(figsize=(15, 12), dpi=300,  facecolor='#0e1117')
ax4.set_facecolor(color='#0e1117')
ax4.bar(avg_working_hour[:, 1], avg_working_hour[:, 0], align='center', color='#4adede', label='Average Time', edgecolor='white')

ax4.set_xlabel('Rating Range', fontsize=20, color='white')
ax4.set_ylabel('Time', fontsize=20, color='white')

ax4.xaxis.set_tick_params(labelsize=16, labelcolor='white', rotation=45)
ax4.yaxis.set_tick_params(labelsize=16, labelcolor='white')
ax4.legend(fontsize=16)
ax4.spines['top'].set_color('white')
ax4.spines['right'].set_color('white')
ax4.spines['bottom'].set_color('white')
ax4.spines['left'].set_color('white')

# Show the plot
st.pyplot(fig4)
