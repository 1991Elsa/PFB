import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
#from limpieza_df import df_nasdaq_tickers_info_clean, df_nasdaq_tickers_historic_clean
from descarga_sql import nasdaq_tickers_historic


# df_nasdaq_tickers_historic_clean = pd.read_csv('historic_clean.csv')

# Título de la herramienta
st.title("🔄 Comparador de Rendimiento y Correlación de Acciones")

# Selección múltiple de tickers
tickers_seleccionados = st.multiselect(
    "Selecciona los tickers que deseas comparar",
    nasdaq_tickers_historic['Ticker'].unique()
)

# Selección de período
st.subheader("📅 Selección de Período")
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

    # Mostrar tabla de rendimientos acumulados
    st.subheader("📊 Rendimiento Acumulado")
    rendimientos_acumulados = rendimientos.groupby('Ticker')['Rendimiento'].sum().reset_index()
    st.dataframe(rendimientos_acumulados)

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

else:
    st.warning("Por favor, selecciona al menos un ticker para comparar.")