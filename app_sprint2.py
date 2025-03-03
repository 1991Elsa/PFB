import streamlit as st
import pandas as pd
from PIL import Image
from modules.pfb_page_config_dict import PAGE_CONFIG
from streamlit_modules import exploratory_data_analysis, comparador_activos1, powerbi, clustering, esquema, about_us
from descarga_sql import descargar_data_sql

# Configuración de la página
st.set_page_config(**PAGE_CONFIG)

# Usamos session_state para agilizar la carga de datos entre páginas
if 'nasdaq_tickers_historic' not in st.session_state or 'nasdaq_tickers_info' not in st.session_state:
    st.session_state.nasdaq_tickers_historic, st.session_state.nasdaq_tickers_info = descargar_data_sql()

nasdaq_tickers_historic = st.session_state.nasdaq_tickers_historic
nasdaq_tickers_info = st.session_state.nasdaq_tickers_info

# Carga la página por defecto en "Inicio"
if 'seccion' not in st.session_state:
    st.session_state.seccion = "Inicio"

# Menu lateral
def sidebar():
    st.sidebar.image("sources/logo_ndq.jpeg", width=50)
    st.sidebar.title("NASDAQ-100")
    st.sidebar.write("")

    pages = [
        "Inicio",
        "Exploratory Data Analysis",
        "Comparador de activos",
        "Dashboard Power BI",
        "Clasificación y clustering",
        "Diagrama de Entidad-Relación",
        "About us"
    ]
  
    st.session_state.seccion = st.sidebar.radio(
        "Elige una sección:",
        pages,
        index=pages.index(st.session_state.seccion)
    )
    st.sidebar.markdown("---")
    if "Timestamp_extraction" in nasdaq_tickers_info:
        st.sidebar.success(f'Última actualización: {nasdaq_tickers_info["Timestamp_extraction"].iloc[0]}')

# Función para mostrar la página de Inicio
def mostrar_inicio():
    st.markdown("<h1 style='text-align: center;'>Bienvenido a la applicación de Nasdaq 100.</h1>", unsafe_allow_html=True)
    st.write("")
    st.image("sources/Nasdaq100.png", use_container_width=False)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.header("**¿Qué es el NASDAQ 100?**")
    st.write("El NASDAQ 100 es un índice bursátil que agrupa a las 100 empresas más importantes de EE.UU. fuera del sector financiero, siendo el sector tecnológico el más representativo.")   
    st.write("")
    st.write("")
    st.subheader("¿Qué secciones encontrarás en esta app?")
    st.markdown(""" 
                - **Exploratory Data Analysis:** Un analísis de datos clave de las empresas del NASDAQ 100 con distintos gráficos y métricas.
                - **Comparador de Activos:** Herramienta muy útil para comparar distintas empresas entre sí.
                - **Dashboard Power BI:** Un tablero interactivo en el que profundizar en las tendencias del mercado.
                - **Modelos de Clasificación y Clustering** para encontrar patrones y clasificar empresas según comportamientos.
                - **Esquema de muestra BBDD**: visualización de la estructura de Entidad Relación de las tablas.
                - **About us:** Un espacio donde se menciona a los integrantes de este proyecto.""")

# Función principal
def main():
    
    sidebar()

    # Página  según la selección del sidebar
    if st.session_state.seccion == "Inicio":
        mostrar_inicio()
    elif st.session_state.seccion == "Exploratory Data Analysis":
        exploratory_data_analysis.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "Comparador de activos":
        comparador_activos1.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "PowerBI":
        powerbi.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "Clasificación y clustering":
        clustering.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "Diagrama de Entidad-Relación":
        esquema.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "About us":
        esquema.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)

if __name__ == "__main__":
    main()
