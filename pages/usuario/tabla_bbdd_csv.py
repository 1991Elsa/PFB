import streamlit as st
import pandas as pd

def mostrar():
    st.title("Visualización de Tablas")
    st.write("")
    
    # Ejemplo de visualización de datos
    st.subheader("📋 Tabla Nasdaq Tickers Información")
    nasdaq_tickers_info = pd.read_csv("nasdaq_tickers_info_clean.csv")
    st.dataframe(nasdaq_tickers_info)

    
    st.subheader("📋 Tabla Nasdaq Tickers Históricos")
    nasdaq_tickers_historic = pd.read_csv("nasdaq_tickers_historic_clean.csv")
    st.dataframe(nasdaq_tickers_historic)