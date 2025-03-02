import streamlit as st
from PIL import Image

# Función para mostrar la página

def esquema_tablasmostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("Esquema de Tablas de la BBDD.")
    st.image("sources/bbdd.PNG", use_container_width=True)