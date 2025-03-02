import streamlit as st
import pandas as pd
from PIL import Image
from modules.pfb_page_config_dict import PAGE_CONFIG
from streamlit_modules import analisis_tecnico, comparador_activos, dashboard_func, esquema, powerbi, tabla_bbdd
from descarga_sql import descargar_data_sql

# Configuración de la página
st.set_page_config(**PAGE_CONFIG)

# Cargar datos si no existen en session_state
if 'nasdaq_tickers_historic' not in st.session_state or 'nasdaq_tickers_info' not in st.session_state:
    st.session_state.nasdaq_tickers_historic, st.session_state.nasdaq_tickers_info = descargar_data_sql()

# Obtener datos
nasdaq_tickers_historic = st.session_state.nasdaq_tickers_historic
nasdaq_tickers_info = st.session_state.nasdaq_tickers_info

# Si aún no se ha seleccionado una página, por defecto es "Inicio"
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Inicio"

# Función para mostrar el sidebar
def sidebar():
    st.sidebar.image("sources/logo_ndq.jpeg", width=50)
    st.sidebar.title("NASDAQ-100")
    st.sidebar.write("")
    # Lista de opciones: incluye "Inicio" y las demás secciones
    pages = [
        "Inicio",
        "Dashboard interactivo",
        "Comparador de activos",
        "Análisis técnico",
        "Tablas BBDD",
        "PowerBI",
        "Esquema de tablas"
    ]
    # Mostrar selector de páginas en el sidebar y actualizar session_state
    st.session_state.selected_page = st.sidebar.radio(
        "Elige una sección:",
        pages,
        index=pages.index(st.session_state.selected_page)
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
    # Mostrar siempre el sidebar
    sidebar()

    # Renderizar la página principal según la selección del sidebar
    if st.session_state.selected_page == "Inicio":
        mostrar_inicio()
    elif st.session_state.selected_page == "Dashboard interactivo":
        dashboard_func.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.selected_page == "Comparador de activos":
        comparador_activos.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.selected_page == "Análisis técnico":
        analisis_tecnico.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.selected_page == "Tablas BBDD":
        tabla_bbdd.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
    elif st.session_state.selected_page == "PowerBI":
        powerbi.mostrar()
    elif st.session_state.selected_page == "Esquema de tablas":
        esquema.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)

if __name__ == "__main__":
    main()
