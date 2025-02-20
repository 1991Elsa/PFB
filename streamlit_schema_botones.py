import streamlit as st
import pandas as pd
import yfinance as yf   
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import mplfinance as mpf
from datetime import datetime
from modules.pfb_page_config_dict import PAGE_CONFIG
from funciones_economicas import *
from connect_engine import get_engine_database
from descarga_sql import descargar_data_sql

# Llamar a la función para obtener los datos
nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

st.set_page_config(**PAGE_CONFIG) 

# Función para la pantalla de inicio
def mostrar_inicio():
    st.header("Inicio")
    st.image(Image.open("sources/logo_ndq.jpeg"), width=50)
    st.title("NASDAQ 100")
    st.write("En esta aplicación podrás visualizar la información de los tickers del NASDAQ 100, así como su evolución en el tiempo y algunas métricas financieras.")  

# Funciones para vista de usuario
def dashboard_interactivo():
    st.title("Dashboard interactivo")
    # código para el Dashboard interactivo

def comparador_activos():
    st.title("Comparador de Rendimiento y Correlación de Acciones")
    # código para el Comparador de activos

def analisis_tecnico():
    st.title("Análisis técnico")
    # código para el Análisis técnico

def tabla_bbdd():
    st.title("Tablas de la Base de Datos")
    st.subheader("Datos Información Tickers")
    st.dataframe(nasdaq_tickers_info)
    st.subheader("Datos Históricos de Tickers")
    st.dataframe(nasdaq_tickers_historic)

# Funciones para vista cliente
def powerbi():
    st.title("Dashboard PowerBI")
    # Subir un archivo de Power BI y visualizar desde Streamlit

def esquema_tablas():
    st.title("Contenido del Esquema relacional BBDD")

# Interfaz principal
def main():
    st.sidebar.title("Navegación")
    st.sidebar.success(f'Last update: \n\n{nasdaq_tickers_info["Timestamp_extraction"][1]}')

    if 'page' not in st.session_state:
        st.session_state['page'] = 'Inicio'

    st.sidebar.button("Inicio", on_click=lambda: st.session_state.update(page='Inicio'))
    st.sidebar.button("Usuario", on_click=lambda: st.session_state.update(page='Usuario'))
    st.sidebar.button("Cliente", on_click=lambda: st.session_state.update(page='Cliente'))

    # Cargar la vista según el estado actual de la página
    if st.session_state.page == 'Inicio':
        mostrar_inicio()
    elif st.session_state.page == 'Usuario':
        opcion_usuario = st.sidebar.radio("Selecciona una sección de usuario", ["Dashboard interactivo", "Comparador de activos", "Análisis técnico", "Tabla de BBDD"], key="usuario")
        if opcion_usuario == "Dashboard interactivo":
            dashboard_interactivo()
        elif opcion_usuario == "Comparador de activos":
            comparador_activos()
        elif opcion_usuario == "Análisis técnico":
            analisis_tecnico()
        elif opcion_usuario == "Tabla de BBDD":
            tabla_bbdd()
    elif st.session_state.page == 'Cliente':
        opcion_cliente = st.sidebar.radio("Selecciona una sección de cliente", ["PowerBI", "Esquema de tablas"], key="cliente")
        if opcion_cliente == "PowerBI":
            powerbi()
        elif opcion_cliente == "Esquema de tablas":
            esquema_tablas()

if __name__ == "__main__":
    main()
