import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
    page_title='Quera Project',
    page_icon='./images/icon.jpg'
)


st.title("First project of the quera data analysis bootcamp")

image = plt.imread('./images/logo.jpg')
st.image(image)

