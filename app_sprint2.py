import streamlit as st
import pandas as pd
from PIL import Image
from modules.pfb_page_config_dict import PAGE_CONFIG
from streamlit_modules import analisis_tecnico1, comparador_activos1,dashboard_func1, esquema1, exploratory_data_analysis, powerbi, tabla_bbdd1
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
        "Dashboard Interactivo",
        "Comparador de activos",
        "Análisis técnico",
        "Tablas BBDD",
        "Dashboard Power BI",
        "Esquema de tablas",
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
    st.markdown("<h1 style='text-align: center;'>Bienvenido a la aplicación de Nasdaq 100.</h1>", unsafe_allow_html=True)
    st.write("")
    st.image("sources/Nasdaq100.png", use_container_width=False)
    st.write("")
    st.subheader("En esta aplicación podrás visualizar la información de los tickers del NASDAQ 100, así como su evolución en el tiempo y algunas métricas financieras.")

# Función principal
def main():
    
    sidebar()

    # Página  según la selección del sidebar
    if st.session_state.seccion == "Inicio":
        mostrar_inicio()
    elif st.session_state.seccion == "Exploratory Data Analysis":
        exploratory_data_analysis.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "Dashboard Interactivo":
        dashboard_func1.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    
    elif st.session_state.seccion == "Comparador de activos":
        comparador_activos1.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "Análisis técnico":
        analisis_tecnico1.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "Tablas BBDD":
        tabla_bbdd1.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "PowerBI":
        powerbi.mostrar()
    elif st.session_state.seccion == "Esquema de tablas":
        esquema1.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.seccion == "About us":
        esquema1.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)

if __name__ == "__main__":
    main()
