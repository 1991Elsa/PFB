import pandas as pd
import numpy as np
import pickle
import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
#from modules.MySQL.descarga_sql import descargar_data_sql


def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("📚​ Clustering y Clasificación")

    st.write("\n")
    st.subheader("Clustering")
  
    with open('nasdaq_tickers_historic_cluster.pkl', 'rb') as file:
            modelo = pickle.load(file)

    valid_clusters = sorted(modelo["Cluster"].dropna().unique())
    valid_clusters = [c for c in valid_clusters if c != -1]

    fig = px.scatter(
        modelo,
        x="Date",
        y = "Ticker",
        color="Cluster",
        title="Cluster de acciones",
        labels={"Date": "Fecha", "Ticker": "Ticker", "Cluster": "Cluster"},
        category_orders={"Cluster": valid_clusters},
        hover_data=["Ticker", "Date", "Cluster"]
    )

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Ticker",
        legend_title="Cluster",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("\n")

    with open('resultados_cluster.pkl', 'rb') as file:
            resultados = pickle.load(file)

    st.markdown("**Conclusiones**")
    for conclusiones in resultados["Conclusiones"]:
        st.write(conclusiones)
    
    st.write("\n")
    st.write("\n")

    st.subheader("Clasificación")

    st.write("\n")

    def cargar_modelo():
        
        with open('scaler_clasification.pkl', 'rb') as file:
            scaler = pickle.load(file)

        with open('modelo_clasification.pkl', 'rb') as file:
            modelo = pickle.load(file)

        return scaler, modelo

    scaler, modelo = cargar_modelo()

    feature_names = ["Close", "High", "Low", "Open"]

    st.markdown("**Predicción de cluster para Acciones**")

    st.write("\n")

    input_data = {}
    columns = st.columns(4)

    for i, feature in enumerate(feature_names):
        with columns[i % 4]:
            input_data[feature] = st.number_input(f"Ingrese el valor de {feature}", value=0.0)

    st.write("\n")

    if st.button("Predecir Clúster"):
        df_input = pd.DataFrame([input_data])

        try:

            data_scaled = scaler.transform(df_input)

            cluster_predicho = int(modelo.predict(data_scaled)[0])

            st.success(f"El cluster predicho es: {cluster_predicho}")

        except Exception as e:
            st.error(f"Error al predecir el cluster: {e}")
