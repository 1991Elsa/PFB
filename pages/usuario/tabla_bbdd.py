import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
#from descarga_sql import descargar_data_sql

def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("Visualización de Tablas")
    st.write("")
    
    # Para nasdaq_tickers_info:
    if nasdaq_tickers_info.index.name == 'Ticker' or 'Ticker' not in nasdaq_tickers_info.columns:
        nasdaq_tickers_info = nasdaq_tickers_info.reset_index()
    if 'Ticker' in nasdaq_tickers_info.columns:
        cols = ['Ticker'] + [col for col in nasdaq_tickers_info.columns if col != 'Ticker']
        nasdaq_tickers_info = nasdaq_tickers_info[cols]
    
    # Ajustar el índice para que empiece en 1
    nasdaq_tickers_info.index = nasdaq_tickers_info.index + 1
    
    st.subheader("📋 Información de las 100 empresas que forman el índice Nasdaq-100")
    st.dataframe(nasdaq_tickers_info.style.highlight_max(axis=0))
    
    st.write("\n")
    st.write("\n")
    
    # Para nasdaq_tickers_historic:
    if nasdaq_tickers_historic.index.name == 'Ticker' or 'Ticker' not in nasdaq_tickers_historic.columns:
        nasdaq_tickers_historic = nasdaq_tickers_historic.reset_index()
    if 'Ticker' in nasdaq_tickers_historic.columns:
        cols = ['Ticker'] + [col for col in nasdaq_tickers_historic.columns if col != 'Ticker']
        nasdaq_tickers_historic = nasdaq_tickers_historic[cols]
    
    # Ajustar el índice para que empiece en 1
    nasdaq_tickers_historic.index = nasdaq_tickers_historic.index + 1
    
    st.subheader("📋 Precios históricos de las 100 empresas que forman el índice Nasdaq-100")
    st.dataframe(nasdaq_tickers_historic)
    
    st.write("\n")
    st.write("\n")


    