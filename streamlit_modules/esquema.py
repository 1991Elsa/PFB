import streamlit as st
from PIL import Image

# Función para mostrar la página

def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("Diagrama de Entidad - Relación")
    st.image("sources/yahoo_finance_nasdaq_100.png", use_container_width=True)
    