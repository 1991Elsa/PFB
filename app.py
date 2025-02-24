import streamlit as st
import pandas as pd
from PIL import Image
from modules.pfb_page_config_dict import PAGE_CONFIG
from descarga_sql import descargar_data_sql

st.set_page_config(**PAGE_CONFIG)

# Cargando los datos desde archivo CSV
nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

# barra lateral
def mostrar_sidebar():
    
    with st.sidebar.expander("Menú de Navegación", expanded=True):
        if st.sidebar.button("INICIO"):
            st.session_state.page = "inicio"

        st.sidebar.title("NASDAQ-100")
        st.sidebar.image("sources/logo_ndq.jpeg", width=50)
        st.sidebar.success(f'Last update: {nasdaq_tickers_info["Timestamp_extraction"][1]}')
       
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

    

# Función para mostrar la página de inicio
def mostrar_inicio():
    st.markdown("<h1 style='text-align: center;'>Bienvenido a la aplicación de Nasdaq 100.</h1>", unsafe_allow_html=True)
    st.write("")
    st.image("sources/Nasdaq100.png", use_container_width=True)
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
                from pages.usuario import dashboard_func
                dashboard_func.mostrar()
            elif st.session_state.sub_page == "Comparador de activos":
                from pages.usuario import comparador_activos
                comparador_activos.mostrar()
            elif st.session_state.sub_page == "Análisis técnico":
                from pages.usuario import analisis_tecnico
                analisis_tecnico.mostrar()
            elif st.session_state.sub_page == "Tablas BBDD":
                from pages.usuario import tabla_bbdd
                tabla_bbdd.mostrar()
    elif st.session_state.page == "cliente":
        if 'sub_page' in st.session_state:
            if st.session_state.sub_page == "PowerBI":
                from pages.cliente import powerbi
                powerbi.mostrar()
            elif st.session_state.sub_page == "Esquema de tablas":
                from pages.cliente import esquema_tablas
                esquema_tablas.mostrar()

if __name__ == "__main__":
    main()
