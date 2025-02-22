import streamlit as st
import pandas as pd
import numpy as np
from descarga_sql import descargar_data_sql

def mostrar():

    nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

    st.title("Visualización de Tablas")
    st.write("")
    
    # Ejemplo de visualización de datos
    st.subheader("📋 Tabla Nasdaq Tickers Información")
    with st.expander("📋 Mostrar tabla"):
        nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()
        st.dataframe(nasdaq_tickers_info.select_dtypes(include=np.number).style.highlight_max(axis=0))

    st.markdown("**Explicación de la Tabla Nasdap Tickers Información**")
    with st.expander("Mostrar explicación de la Tabla"):
        st.text("""La tabla muestra información general de las 100 empresas que forman parte del índice Nasdap-100.""")


    st.write("\n")
    
    st.subheader("📋 Tabla Nasdaq Tickers Históricos")
    with st.expander("📋 Mostrar tabla"):
        nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()
        st.dataframe(nasdaq_tickers_historic)

    st.markdown("**Explicación de la Tabla Nasdap Tickers Históricos**")
    with st.expander("Mostrar explicación de la Tabla"):
        st.text("""La tabla muestra información historica en los últimos 10 años de las 100 empresas que forman parte del índice Nasdap-100.""")

    