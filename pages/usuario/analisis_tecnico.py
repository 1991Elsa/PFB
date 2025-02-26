import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
#from descarga_sql import descargar_data_sql

# Cargar datos desde archivo CSV y cambiar type columnas
#nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

# Función para mostrar la página
def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("📊 Análisis Técnico")

    st.write("\n")
    st.write("\n")

    # Selección de ticker
    ticker_seleccionado = st.selectbox("Selecciona un ticker", nasdaq_tickers_historic['Ticker'].unique())

    st.write("\n")
    st.write("\n")

    # Selección de período
    st.header("📅 Selección de Período")

    st.write("\n")

    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha de inicio", datetime(2020, 1, 1))
    with col2:
        fecha_fin = st.date_input("Fecha de fin", datetime.today())

    # Convertir las fechas a datetime
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Filtrar los datos por el período seleccionado
    df_ticker = nasdaq_tickers_historic[(nasdaq_tickers_historic['Ticker'] == ticker_seleccionado) & 
                                        (nasdaq_tickers_historic['Date'] >= fecha_inicio) & 
                                        (nasdaq_tickers_historic['Date'] <= fecha_fin)]

    if df_ticker.empty:
        st.warning("No hay datos disponibles para el ticker seleccionado en el período especificado.")
        return

    st.write("\n")
    
    # Calcular y mostrar el ROI, Sharpe Ratio y Sortino Ratio en columnas
    col1, col2, col3 = st.columns(3)
    with col1:
        roi_value = roi(ticker_seleccionado, fecha_inicio, fecha_fin, nasdaq_tickers_historic)
        st.metric(label="ROI (%)", value=roi_value)
    with col2:
        sharpe = sharpe_ratio(ticker_seleccionado, fecha_inicio, fecha_fin, nasdaq_tickers_historic)
        st.metric(label="Sharpe Ratio", value=sharpe)
    with col3:
        sortino = sortino_ratio(ticker_seleccionado, fecha_inicio, fecha_fin, nasdaq_tickers_historic)
        st.metric(label="Sortino Ratio", value=sortino)

    st.write("\n")
    st.write("\n")

    st.subheader("Tabla de Volatilidad")
    # Mostrar la volatilidad
  
    st.write("Esta tabla muestra la volatilidad de cada ticker seleccionado durante el período especificado.")
    volatilidad = calcular_volatilidad(nasdaq_tickers_historic)
    st.dataframe(volatilidad.select_dtypes(include=np.number).style.highlight_max(axis=0))

    
    with st.expander("Mostrar explicación de la tabla de volatilidad"):
        st.text(""" La volatilidad mide cuánto varía el precio de un activo en un período determinado. \n
                Un activo con alta volatilidad tiene cambios bruscos en su precio, mientras que uno con baja volatilidad es más estable. \n
                La tabla muestra en color amarillo los activos más volátiles; es decir, menos estables.""")


    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    

    # Mostrar la correlación
    st.subheader("Matriz de Correlación")
    st.write("Esta tabla muestra la matriz de correlación entre los tickers seleccionados, indicando cómo se relacionan los precios de cierre entre ellos.")
    correlacion = calcular_correlacion(nasdaq_tickers_historic)
    st.dataframe(correlacion.select_dtypes(include=np.number).style.highlight_max(axis=0))
    
    with st.expander("Mostrar explicación de la Matriz de Correlación"):
        st.text(""" Correlación positiva (cercana a +1): Las acciones tienden a moverse en la misma dirección.
        Correlación negativa (cercana a -1): Las acciones tienden a moverse en direcciones opuestas.
        Correlación cercana a 0: Hay poca o ninguna relación entre los movimientos de las acciones.""")

    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")

# Resto de funciones (roi, sharpe_ratio, sortino_ratio, calcular_volatilidad, calcular_correlacion) permanecen iguales

# Función para calcular el ROI
def roi(ticker, fecha_inicial, fecha_final, df):
    fecha_inicial = pd.to_datetime(fecha_inicial)
    fecha_final = pd.to_datetime(fecha_final)
    df_ticker = df[(df['Ticker'] == ticker) & (df['Date'].between(fecha_inicial, fecha_final))]

    if df_ticker.empty:
        return "No hay datos disponibles"

    precio_inicial = df_ticker.iloc[0]['Close']
    precio_final = df_ticker.iloc[-1]['Close']

    if pd.isna(precio_inicial) or pd.isna(precio_final):
        return "Datos faltantes"

    roi_value = ((precio_final - precio_inicial) / precio_inicial) * 100
    return round(roi_value, 2)

# Función para calcular el Sharpe Ratio
def sharpe_ratio(ticker, start_date, end_date, df, risk_free_rate=0.02):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_ticker = df[(df['Ticker'] == ticker) & (df['Date'].between(start_date, end_date))].sort_values(by='Date')

    if df_ticker.shape[0] < 2:
        return "Datos insuficientes"

    df_ticker['Rendimiento Diario'] = df_ticker['Close'].pct_change(fill_method=None)
    mean_daily_return = df_ticker['Rendimiento Diario'].mean()
    std_dev_daily_return = df_ticker['Rendimiento Diario'].std()
    mean_annual_return = mean_daily_return * 252
    std_dev_annual_return = std_dev_daily_return * np.sqrt(252)

    if std_dev_annual_return == 0 or pd.isna(std_dev_annual_return):
        return "Volatilidad no definida"

    sharpe = (mean_annual_return - risk_free_rate) / std_dev_annual_return
    return round(sharpe, 2)

# Función para calcular el Sortino Ratio
def sortino_ratio(ticker, start_date, end_date, df, risk_free_rate=0.02):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_ticker = df[(df['Ticker'] == ticker) & (df['Date'].between(start_date, end_date))].sort_values(by='Date')

    if df_ticker.shape[0] < 2:
        return "Datos insuficientes"

    df_ticker['Rendimiento Diario'] = df_ticker['Close'].pct_change(fill_method=None)
    mean_daily_return = df_ticker['Rendimiento Diario'].mean()
    mean_annual_return = mean_daily_return * 252
    downside_returns = df_ticker['Rendimiento Diario'][df_ticker['Rendimiento Diario'] < 0]
    downside_deviation = downside_returns.std() * np.sqrt(252)

    if downside_deviation == 0 or pd.isna(downside_deviation):
        return "Volatilidad negativa no definida"

    sortino = (mean_annual_return - risk_free_rate) / downside_deviation
    return round(sortino, 2)

# Función para calcular la volatilidad
def calcular_volatilidad(df, periodo="diario"):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Rentabilidad'] = df.groupby('Ticker')['Close'].pct_change(fill_method=None)

    if periodo == "mensual":
        df['Month'] = df['Date'].dt.to_period('M')
        datos_mensuales = df.groupby(['Ticker', 'Month'])['Close'].last().pct_change(fill_method=None)
        volatilidad = datos_mensuales.groupby('Ticker').std().reset_index()
    elif periodo == "diario":
        volatilidad = df.groupby('Ticker')['Rentabilidad'].std().reset_index()
    else:
        raise ValueError("El periodo debe ser 'diario' o 'mensual'.")

    volatilidad.columns = ['Ticker', 'Volatilidad']
    volatilidad = volatilidad.sort_values(by="Volatilidad", ascending=False).reset_index(drop=True)
    return volatilidad

# Función para calcular la correlación
def calcular_correlacion(df, periodo="diario"):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Ticker'].isin(df["Ticker"].unique().tolist())]
    df['Rentabilidad'] = df.groupby('Ticker')['Close'].pct_change(fill_method=None)

    if periodo == "mensual":
        df['Month'] = df['Date'].dt.to_period('M')
        datos_mensuales = df.groupby(['Ticker', 'Month'])['Close'].last().pct_change()
        matriz_correlacion = datos_mensuales.unstack().corr()
    elif periodo == "diario":
        matriz_rentabilidades = df.pivot(index="Date", columns="Ticker", values="Rentabilidad")
        matriz_correlacion = matriz_rentabilidades.corr()
    else:
        raise ValueError("El periodo debe ser 'diario' o 'mensual'.")

    return matriz_correlacion

    
