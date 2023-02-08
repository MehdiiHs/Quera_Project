import streamlit as st
import mysql.connector as mysql
import traceback
from utils.CRUD import read, connect


st.set_page_config(
    page_title='Quera Project',
    page_icon= ':panda:'
)

st.title("First project of the quera data analysis bootcamp")


con = connect()
st.write(read(con, 'cafe_df'))

