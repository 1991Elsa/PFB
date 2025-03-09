import streamlit as st
from descarga_sql import descargar_data_sql


def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("Clasificación y Clustering")
   