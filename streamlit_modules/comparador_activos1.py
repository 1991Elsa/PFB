import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
# from descarga_sql import descargar_data_sql

def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    # nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()
    #nasdaq_tickers_historic = pd.read_csv("nasdaq_tickers_historic_clean.csv")

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

    # Definimos fecha mínima y máxima para el selector de calendario
    fecha_minima = datetime(2010, 1, 1)  # 01/01/2010
    fecha_maxima = datetime.today()  # Fecha actual

    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha de inicio", datetime(2020, 1, 1), min_value=fecha_minima, max_value=fecha_maxima)
    with col2:
        fecha_fin = st.date_input("Fecha de fin", datetime.today(), min_value=fecha_minima, max_value=fecha_maxima)


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
        st.write('\n')
        #st.write('\n')
        #st.write("\n")

        # --- Comparación de rendimientos ---
        st.subheader("📈 Comparación de Rendimientos")
        
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

        st.markdown("""
📘Explicación del Gráfico de Comparación de Rendimientos.

Este gráfico muestra como han cambiado los rendimientos de diferentes activos a lo largo del tiempo en la misma escala porcentual.

En general, se observa:
- Qué acción ha tenido mejor desempeño en un período de tiempo específico.
- Cuánto ha crecido o caído una inversión inicial en diferentes activos a lo largo del tiempo.         
---""")
           


        # Mostrar tabla de rendimientos acumulados
        st.subheader("📊 Rendimiento Acumulado")
        rendimientos_acumulados = rendimientos.groupby('Ticker')['Rendimiento'].sum().reset_index()
        rendimientos_acumulados.set_index('Ticker', inplace=True)
        st.dataframe(rendimientos_acumulados.select_dtypes(include=np.number).style.highlight_max(axis=0))


        st.markdown("""
📘Explicación del Rendimiento Acumulado.
                    
- Se refiere a la ganancia o pérdida total de una inversión durante un período determinado, expresado en porcentaje.
- En color amarillo se muestra el valor más alto obtenido de rendimiento acumulado.
---""")

        # --- Gráfico de correlación ---
        st.subheader("📊 Correlación entre las Acciones Seleccionadas")
        
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

        st.markdown("""
📘 Explicación del Gráfico de Correlación.

Este gráfico muestra la relación entre los precios de cierre de los tickers seleccionados.

🔹 ¿Para qué se usa la correlación entre acciones?

La <strong>diversificación de portafolios</strong> se puede evaluar observando los movimientos de las acciones:

- Un valor cercano a <strong>-1</strong> indica que tienden a moverse en direcciones opuestas, lo que puede ayudar a reducir el riesgo en un portafolio.
- Un valor cercano a <strong>1</strong> indica que las acciones tienden a moverse en la misma dirección, sus movimientos son similares, lo que no ayuda mucho a diversificar.
- Un valor cercano a <strong>0</strong> indica poca o ninguna relación entre los movimientos de las acciones, lo que también puede ser útil para diversificación.

A la hora de gestionar riesgos, los inversores pueden usar la correlación para evitar una exposición excesiva a inversiones en activos que se comporten de manera similar.

<p style="font-weight: normal;">Este análisis es clave para evaluar cómo interactúan diferentes activos en un portafolio y optimizar la estrategia de inversión. 🚀📈</p>
---
""", unsafe_allow_html=True)
        
    

    else:
        st.warning("Por favor, selecciona al menos un ticker para comparar.")