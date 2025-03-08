import pandas as pd
import numpy as np
import pickle
import streamlit as st

def cargar_modelo():
     
     with open('scaler_clasification.pkl', 'rb') as file:
        scaler = pickle.load(file)

     with open('modelo_clasification.pkl', 'rb') as file:
        modelo = pickle.load(file)

     return scaler, modelo

modelo, scaler = cargar_modelo()

feature_names = ["Close", "High", "Low", "Open"]

st.title("Predicción de cluster para Acciones")

input_data = {}
for feature in feature_names:
    input_data[feature] = st.number_input(f"Ingrese el valor de {feature}", value=0.0)

if st.botton("Predecir Clúster"):
    df_input = pd.DataFrame([input_data])

    data_scaler = scaler.transform(df_input)

    cluster_predicho = modelo.predict(data_scaler)[0]

    st.success(f"El cluster predicho es: {cluster_predicho}")