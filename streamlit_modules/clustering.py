import pandas as pd
import numpy as np
import pickle
import streamlit as st
from modules.MySQL.descarga_sql import descargar_data_sql  

def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("📚​ Clustering y Clasificación de Acciones")

    # Cargar modelos
    def cargar_modelo():
        with open('scaler_clasification.pkl', 'rb') as file:
            scaler = pickle.load(file)
        with open('modelo_clasification.pkl', 'rb') as file:
            modelo = pickle.load(file)
        return scaler, modelo

    scaler, modelo = cargar_modelo()

    st.markdown("### Predicción de clúster para una acción")
    
    # Crear un selector de empresas
    tickers_disponibles = nasdaq_tickers_historic["Ticker"].unique().tolist()
    ticker_seleccionado = st.selectbox("Seleccione una empresa", tickers_disponibles)

    if st.button("Predecir Clúster"):
        # Buscar los valores reales de la empresa seleccionada
        datos_empresa = nasdaq_tickers_historic[nasdaq_tickers_historic["Ticker"] == ticker_seleccionado].iloc[-1]
        
        valores = datos_empresa[["Close", "High", "Low", "Open"]].values.reshape(1, -1)

        # Transformar los valores con el scaler
        valores_escalados = scaler.transform(valores)

        # Predecir el clúster
        cluster_predicho = int(modelo.predict(valores_escalados)[0])

        st.success(f"El cluster de {ticker_seleccionado} es: {cluster_predicho}")

