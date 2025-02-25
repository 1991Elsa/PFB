import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from descarga_sql import descargar_data_sql

def mostrar():

    nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

    st.title("Visualización de Tablas")
    st.write("")
    
    # Ejemplo de visualización de datos
    st.subheader("📋 Información de las 100 empresas que forman el índice Nasdap-100")
    with st.expander("📋 Mostrar información"):
        nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()
        st.dataframe(nasdaq_tickers_info.select_dtypes(include=np.number).style.highlight_max(axis=0))

    

    st.write("\n")
    st.write("\n")
    
    st.subheader("📋 Precios historicos de las 100 empresas que forman el índice Nasdap-100")
    with st.expander("📋 Mostrar tabla"):
        nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()
        st.dataframe(nasdaq_tickers_historic)


    st.write("\n")
    st.write("\n")

    