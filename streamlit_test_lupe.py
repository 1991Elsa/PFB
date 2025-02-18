import streamlit as st
import pandas as pd
import yfinance as yf   
from PIL import Image
import plotly.graph_objects as go
import mplfinance as mpf
from modules.pfb_page_config_dict import PAGE_CONFIG
from funciones_economicas import *
from connect_engine import get_engine_database
from descarga_sql import descargar_data_sql

# Llamar a la función para obtener los datos
nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

st.set_page_config(**PAGE_CONFIG) 

# Funciones para las secciones del menú lateral
def mostrar_inicio():
    st.title("PFB Yahoo Finance")
    st.markdown("""
    ### Bienvenidos
    Aquí encontrarás un resumen de la aplicación.
    """)
    st.image("sources/Yahoo!_finance_fondo.png", use_container_width=True)  

def mostrar_cliente(seccion):
    st.header("Vista Cliente")
    if seccion == "Dashboard PowerBI":
        st.write("Contenido del Dashboard PowerBI")
    elif seccion == "Esquema relacional BBDD":
        st.write("Contenido del Esquema relacional BBDD")

def mostrar_usuario(seccion):
    st.header("Vista Usuario")
    if seccion == "Dashboard Interactivo":
        st.write("Contenido del Dashboard Interactivo")
    elif seccion == "Comparador de Activos":
        st.write("Contenido del Comparador de Activos")
    elif seccion == "Analisis Tecnico":
        st.write("Contenido del Analisis Tecnico")
    elif seccion == "Tabla BBDD":
        st.write("Contenido de la Tabla BBDD")

# Función principal
def main():
    # Configuración de la página inicial
    st.sidebar.title("Menú")

    # Menú lateral inicial para seleccionar entre Usuario y Cliente
    vista_principal = st.sidebar.selectbox("Selecciona una vista:", ["Inicio", "Usuario", "Cliente"])

    # Mostrar contenido dependiendo de la vista principal seleccionada
    if vista_principal == "Empecemos":
        mostrar_inicio()
    elif vista_principal == "Usuario":
        opcion_usuario = st.sidebar.radio("Selecciona una sección de usuario", ["Dashboard Interactivo", "Comparador de Activos", "Analisis Tecnico", "Tabla BBDD"], key="usuario")
        mostrar_usuario(opcion_usuario)
    elif vista_principal == "Cliente":
        opcion_cliente = st.sidebar.radio("Selecciona una sección de cliente", ["Dashboard PowerBI", "Esquema relacional BBDD"], key="cliente")
        mostrar_cliente(opcion_cliente)

if __name__ == "__main__":  
    main() 
