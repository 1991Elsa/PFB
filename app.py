import streamlit as st
import pandas as pd
from PIL import Image
from modules.pfb_page_config_dict import PAGE_CONFIG
from pages.usuario import dashboard_func, comparador_activos, analisis_tecnico, tabla_bbdd
from pages.cliente import powerbi, esquema_tablas
from descarga_sql import descargar_data_sql

st.set_page_config(**PAGE_CONFIG)

# Cargar los datos en st.session_state si no existen
if 'nasdaq_tickers_historic' not in st.session_state or 'nasdaq_tickers_info' not in st.session_state:
    st.session_state.nasdaq_tickers_historic, st.session_state.nasdaq_tickers_info = descargar_data_sql()

# Obtener los datos desde st.session_state
nasdaq_tickers_historic = st.session_state.nasdaq_tickers_historic
nasdaq_tickers_info = st.session_state.nasdaq_tickers_info

# barra lateral
def mostrar_sidebar():
    
    with st.sidebar.expander("Menú de Navegación", expanded=True):
        st.sidebar.image("sources/logo_ndq.jpeg", width=50)
        st.sidebar.title("NASDAQ-100")
        st.sidebar.write("")

        if st.sidebar.button("INICIO"):
            st.session_state.page = "inicio"
        
        # Separador visual
        st.sidebar.markdown("---")

        st.sidebar.write("Selecciona tu vista:")

        # Botón de USUARIO
        if st.sidebar.button("USUARIO"):
            st.session_state.page = "usuario"
            st.session_state.sub_page = None

        if st.session_state.page == "usuario":
            sub_page = st.sidebar.radio("Selecciona una sección de Usuario:", 
                                        ["Dashboard interactivo", "Comparador de activos", "Análisis técnico", "Tablas BBDD"], 
                                        key="usuario")
            st.session_state.sub_page = sub_page

        # Botón de CLIENTE
        if st.sidebar.button("CLIENTE"):
            st.session_state.page = "cliente"
            st.session_state.sub_page = None 

        if st.session_state.page == "cliente":
            sub_page = st.sidebar.radio("Selecciona una sección de Cliente:", 
                                        ["PowerBI", "Esquema de tablas"], 
                                        key="cliente")
            st.session_state.sub_page = sub_page
        
        st.sidebar.markdown("---")

        # Time stamp de actualizacion
        st.sidebar.success(f'Last update: {nasdaq_tickers_info["Timestamp_extraction"][1]}')
       
    

# Función para mostrar la página de inicio
def mostrar_inicio():
    st.markdown("<h1 style='text-align: center;'>Bienvenido a la aplicación de Nasdaq 100.</h1>", unsafe_allow_html=True)
    st.write("")
    st.image("sources/Nasdaq100.png", use_container_width=False)
    st.write("")
    st.subheader("""En esta aplicación podrás visualizar la información de los tickers del NASDAQ 100, así como su evolución en el tiempo y algunas métricas financieras.
    """)

# Función principal
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "inicio"

    mostrar_sidebar()

    if st.session_state.page == "inicio":
        mostrar_inicio()
    elif st.session_state.page == "usuario":
        if 'sub_page' in st.session_state:
            if st.session_state.sub_page == "Dashboard interactivo":
                dashboard_func.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)

            elif st.session_state.sub_page == "Comparador de activos":
                comparador_activos.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)
                
            elif st.session_state.sub_page == "Análisis técnico":
                analisis_tecnico.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)

            elif st.session_state.sub_page == "Tablas BBDD":
                
                tabla_bbdd.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)

    elif st.session_state.page == "cliente":
        if 'sub_page' in st.session_state:
            if st.session_state.sub_page == "PowerBI":
                powerbi.mostrar()
            elif st.session_state.sub_page == "Esquema de tablas":
                esquema_tablas.mostrar(nasdaq_tickers_historic, nasdaq_tickers_info)

if __name__ == "__main__":
    main()