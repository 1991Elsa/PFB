import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from descarga_sql import descargar_data_sql

nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

# Título de la herramienta

def mostrar():

    st.title("🔄 Comparador de Rendimiento y Correlación de Acciones")
    st.write("Usa esta herramienta para comparar el rendimiento y la correlación de acciones del NASDAQ 100.")

    st.write("\n")
    st.write("\n")

    # Selección múltiple de tickers
    tickers_seleccionados = st.multiselect(
        "Selecciona los tickers que deseas comparar",
        nasdaq_tickers_historic['Ticker'].unique()
    )

    st.write('\n')
    st.write('\n')


    # Selección de período
    st.subheader("📅 Selección de Período")
    st.write("Selecciona el período de tiempo para el análisis de rendimiento y correlación.")

    st.write("\n")
    st.write("\n")

    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha de inicio", datetime(2020, 1, 1))
    with col2:
        fecha_fin = st.date_input("Fecha de fin", datetime.today())

    # Convertir las fechas a datetime64[ns] para filtrar el dataframe
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Verificar si se han seleccionado tickers
    if tickers_seleccionados:
        # Filtrar el dataframe por el período seleccionado
        df_filtrado = nasdaq_tickers_historic[
            (nasdaq_tickers_historic['Date'] >= fecha_inicio) &
            (nasdaq_tickers_historic['Date'] <= fecha_fin)
        ]

        st.write("\n")
        st.write("\n")

        # --- Comparación de rendimientos ---
        st.subheader("📈 Comparación de Rendimientos")
        with st.expander("📈 Mostrar Comparación de Rendimientos"):
        
            # Crear un dataframe para almacenar los rendimientos
            rendimientos = pd.DataFrame()

            # Calcular el rendimiento para cada ticker seleccionado
            for ticker in tickers_seleccionados:
                # Filtrar datos para el ticker actual
                df_ticker = df_filtrado[df_filtrado['Ticker'] == ticker]
                
                # Ordenar por fecha (asegurarse de que los datos estén en orden cronológico)
                df_ticker = df_ticker.sort_values('Date')
                
                # Calcular el rendimiento porcentual
                df_ticker['Rendimiento'] = (df_ticker['Close'].pct_change(fill_method=None)) * 100
                
                # Agregar los datos al dataframe de rendimientos
                df_ticker['Ticker'] = ticker  # Añadir columna de ticker para identificarlo
                rendimientos = pd.concat([rendimientos, df_ticker[['Date', 'Ticker', 'Rendimiento']]])

            # Gráfico de rendimientos comparados
            fig_rendimientos = px.line(
                rendimientos,
                x='Date',
                y='Rendimiento',
                color='Ticker',
                title=f"Rendimiento Porcentual de los Tickers Seleccionados ({fecha_inicio.date()} - {fecha_fin.date()})",
                labels={'Rendimiento': 'Rendimiento (%)', 'Date': 'Fecha'}
            )
            st.plotly_chart(fig_rendimientos)
        
        with st.expander("📘Explicación del Gráfico de Comparación de Rendimientos"):
            st.write(""" Este gráfico muestra como han cambiado los rendimientos de diferentes activos a lo largo del tiempo en la misma escala porcentual.
            """)

        # Mostrar tabla de rendimientos acumulados
        st.subheader("📊 Rendimiento Acumulado")
        with st.expander("📊 Mostrar Rendimiento Acumulado"):
            rendimientos_acumulados = rendimientos.groupby('Ticker')['Rendimiento'].sum().reset_index()
            st.dataframe(rendimientos_acumulados.select_dtypes(include=np.number).style.highlight_max(axis=0))

        with st.expander("📘Explicación del Rendimiento Acumulado"):
            st.write("Se refiere a la ganancia o pérdida total de una inversión durante un período determinado, expresado en porcentaje.") 
            st.write("En color amarillo se muestra el valor más alto obtenido de rendimiento acumulado.")

        # --- Gráfico de correlación ---
        st.subheader("📊 Correlación entre las Acciones Seleccionadas")
        with st.expander("📊Mostrar Correlación entre las Acciones Seleccionadas"):

            # Crear un dataframe con los precios de cierre de los tickers seleccionados
            precios_cierre = pd.DataFrame()

            for ticker in tickers_seleccionados:
                df_ticker = df_filtrado[df_filtrado['Ticker'] == ticker]
                df_ticker = df_ticker.sort_values('Date')
                precios_cierre[ticker] = df_ticker.set_index('Date')['Close']

            # Calcular la matriz de correlación
            matriz_correlacion = precios_cierre.corr()

            # Gráfico de correlación (heatmap) con anotaciones
            fig_correlacion = go.Figure(data=go.Heatmap(
                z=matriz_correlacion.values,
                x=matriz_correlacion.columns,
                y=matriz_correlacion.index,
                colorscale='Viridis',
                zmin=-1,
                zmax=1,
                colorbar=dict(title='Correlación'),
                text=matriz_correlacion.values.round(2),  # Anotaciones con 2 decimales
                texttemplate="%{text}",  # Mostrar el texto en el heatmap
                hoverinfo="none"  # Desactivar información adicional al pasar el mouse
            ))
            fig_correlacion.update_layout(
                title=f"Matriz de Correlación entre las Acciones Seleccionadas ({fecha_inicio.date()} - {fecha_fin.date()})",
                xaxis_title="Ticker",
                yaxis_title="Ticker"
            )
            st.plotly_chart(fig_correlacion)

        with st.expander("📘Explicación del Gráfico de Correlación"):
            st.write("Este gráfico muestra la relación entre los precios de cierre de los tickers seleccionados.")
            st.write("Los valores de correlación varían entre -1 y 1.")
            st.write("Un valor cercano a 1 indica que las acciones tienden a moverse en la misma dirección.")
            st.write("Un valor cercano a -1 indica que tienden a moverse en direcciones opuestas.")
            st.write("Un valor cercano a 0 indica poca o ninguna relación entre los movimientos de las acciones.")

    else:
        st.warning("Por favor, selecciona al menos un ticker para comparar.")