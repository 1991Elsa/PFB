import pandas as pd
import numpy as np
import pickle
import streamlit as st
import pandas as pd
import pickle
import numpy as np
from modules.MySQL.descarga_sql import descargar_data_sql


def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("📚​ Clustering y Clasificación")

    #st.subheader("Clustering")

    #st.subheader("Clasificación")

    def cargar_modelo():
        
        with open('scaler_clasification.pkl', 'rb') as file:
            scaler = pickle.load(file)

        with open('modelo_clasification.pkl', 'rb') as file:
            modelo = pickle.load(file)

        return scaler, modelo

    scaler, modelo = cargar_modelo()

    feature_names = ["Close", "High", "Low", "Open"]

    st.markdown("**Predicción de cluster para Acciones**")

    input_data = {}
    columns = st.columns(4)

    for i, feature in enumerate(feature_names):
        with columns[i % 4]:
            input_data[feature] = st.number_input(f"Ingrese el valor de {feature}", value=0.0)

    if st.button("Predecir Clúster"):
        df_input = pd.DataFrame([input_data])

        try:

            data_scaled = scaler.transform(df_input)

            cluster_predicho = int(modelo.predict(data_scaled)[0])

            st.success(f"El cluster predicho es: {cluster_predicho}")

        except Exception as e:
            st.error(f"Error al predecir el cluster: {e}")
