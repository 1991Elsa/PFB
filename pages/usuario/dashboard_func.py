import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
<<<<<<< HEAD
from descarga_sql import descargar_data_sql
=======
import numpy as np
from datetime import datetime
from descarga_sql import descargar_data_sql

nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()
>>>>>>> main

# Definir las funciones

def roi(ticker, start_date, end_date, df):
    """Función para calcular el ROI (Retorno de la Inversión)"""
    df_ticker = df[df["Ticker"] == ticker]
    df_filtered = df_ticker[(df_ticker["Date"] >= start_date) & (df_ticker["Date"] <= end_date)]
    if df_filtered.empty:
        return 0
    initial_price = df_filtered.iloc[0]["Close"]
    final_price = df_filtered.iloc[-1]["Close"]
    roi_value = ((final_price - initial_price) / initial_price) * 100
    return round(roi_value, 2)

def sharpe_ratio(ticker, start_date, end_date, df, risk_free_rate=0):
    """Función para calcular el Sharpe Ratio"""
    df_ticker = df[df["Ticker"] == ticker]
    df_filtered = df_ticker[(df_ticker["Date"] >= start_date) & (df_ticker["Date"] <= end_date)]
    if df_filtered.empty:
        return 0
    returns = df_filtered["Close"].pct_change().dropna()
    excess_returns = returns - risk_free_rate
    sharpe_ratio_value = excess_returns.mean() / excess_returns.std()
    return round(sharpe_ratio_value, 2)

def sortino_ratio(ticker, start_date, end_date, df, risk_free_rate=0):
    """Función para calcular el Sortino Ratio"""
    df_ticker = df[df["Ticker"] == ticker]
    df_filtered = df_ticker[(df_ticker["Date"] >= start_date) & (df_ticker["Date"] <= end_date)]
    if df_filtered.empty:
        return 0
    returns = df_filtered["Close"].pct_change().dropna()
    downside_returns = returns[returns < 0]
    if downside_returns.empty:
        return 0
    downside_deviation = downside_returns.std()
    excess_returns = returns - risk_free_rate
    sortino_ratio_value = excess_returns.mean() / downside_deviation
    return round(sortino_ratio_value, 2)

def mostrar():
    st.title("Dashboard Interactivo")
    st.write("Este es el contenido del Dashboard Interactivo.")

    # Cargar datos desde archivo CSV
<<<<<<< HEAD

    nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()
    #nasdaq_tickers_info = pd.read_csv("nasdaq_tickers_info_clean.csv")
    #nasdaq_tickers_historic = pd.read_csv("nasdaq_tickers_historic_clean.csv")
=======
    nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()
>>>>>>> main

    # Convertir la columna 'Date' a tipo datetime
    nasdaq_tickers_historic['Date'] = pd.to_datetime(nasdaq_tickers_historic['Date'])

    tickers_nasdaq = nasdaq_tickers_info["Ticker"].unique().tolist()

    st.write("\n")
    st.write("\n")

    selected_ticker = st.selectbox("Selecciona el ticker a mostrar", options=tickers_nasdaq)
    info = nasdaq_tickers_info[nasdaq_tickers_info["Ticker"] == selected_ticker]
    short_name, sector, industry, country, MarketCap = [
        info[col].values[0] if not info[col].empty else "No disponible"
        for col in ["ShortName", "Sector", "Industry", "Country", "MarketCap"]
    ]

    st.write("\n")

    cols = st.columns(5)
    labels = ["Nombre", "Sector", "Industria", "País", 'MarketCap']
    values = [short_name, sector, industry, country, f'{MarketCap / 1_000_000:,.0f} $M']

    for col, label, value in zip(cols, labels, values):
        with col:
            st.write(f"**{label}:** {value}")

    st.write('\n')
    st.write('\n')

    # Selección de período
    st.subheader("📅 Selección de Período")
    st.write("Selecciona el período de tiempo para el análisis.")

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

    # Filtrar datos según el ticker y el rango de fechas
    df_filtrado = nasdaq_tickers_historic[
        (nasdaq_tickers_historic["Ticker"] == selected_ticker) &
        (nasdaq_tickers_historic["Date"] >= fecha_inicio) &
        (nasdaq_tickers_historic["Date"] <= fecha_fin)
    ]

    # Verificar si hay datos para mostrar
    if df_filtrado.empty:
        st.warning("No hay datos disponibles para el rango seleccionado.")
    else:
        # Crear el gráfico de velas
        fig = go.Figure(data=[
            go.Candlestick(
                x=df_filtrado["Date"],
                open=df_filtrado["Open"],
                high=df_filtrado["High"],
                low=df_filtrado["Low"],
                close=df_filtrado["Close"],
                name=selected_ticker
            )
        ])

        # Personalizar el diseño
        fig.update_layout(
            title=f"Gráfico de Velas Japonesas - {selected_ticker} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}",
            xaxis_title="Fecha",
            yaxis_title="Precio",
            xaxis_rangeslider_visible=False,
            template="plotly_dark"
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    df_ticker = nasdaq_tickers_historic[nasdaq_tickers_historic["Ticker"] == selected_ticker].copy()
    df_ticker["SMA"] = df_ticker["Close"].rolling(20).mean()
    df_ticker["Upper"] = df_ticker["SMA"] + 2 * df_ticker["Close"].rolling(20).std()
    df_ticker["Lower"] = df_ticker["SMA"] - 2 * df_ticker["Close"].rolling(20).std()

    fig_bollinger = go.Figure()
    fig_bollinger.update_layout(title=f"Bandas de Bollinger - {selected_ticker} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}")
    title = f"Bandas de Bollinger - {selected_ticker} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}"
    fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Close"], mode="lines", name="Precio"))
    fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["SMA"], mode="lines", name="SMA"))
    fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Upper"], mode="lines", name="Upper Band", line=dict(dash="dot")))
    fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Lower"], mode="lines", name="Lower Band", line=dict(dash="dot")))
    st.plotly_chart(fig_bollinger)

    st.write('\n')
    st.write('\n')

    st.subheader("Métricas")
    with st.expander("Mostrar métricas", expanded=False):
        # Calcular el ROI
        roi_value = roi(selected_ticker, fecha_inicio, fecha_fin, df=nasdaq_tickers_historic)
        st.write(f"**ROI:**")
        if roi_value > 0:
            st.success(f'Invertir en esa acción durante ese período habría generado una ganancia del {roi_value}%')
        elif roi_value < 0:
            st.error(f'Si hubieras invertido en esa acción, habrías perdido un {roi_value}% de tu inversión.')
        st.write('\n')

        # Calcular Sharpe Ratio
        col_risk1, col_risk2, col_risk3, col_risk4, col_risk5 = st.columns(5)
        with col_risk5:
            risk = st.number_input("Introducir riesgo personalizado (%)", min_value=0.0, max_value=100.0, value=20.00, step=0.01)
            risk = risk / 100

        col_sortino, col_sharpe = st.columns(2)

        with col_sharpe:
            sharpe_value = sharpe_ratio(selected_ticker, fecha_inicio, fecha_fin, df=nasdaq_tickers_historic, risk_free_rate=risk)
            st.write(f"**Sharpe Ratio:** {sharpe_value}")
            if sharpe_value > 1:
                st.success('Buena inversión ajustada al riesgo')
            elif sharpe_value < 1:
                st.warning('Riesgo alto en relación con el retorno')
            elif sharpe_value > 2:
                st.success('Excelente inversión')
            elif sharpe_value > 3:
                st.success('Inversión excepcional')

        with col_sortino:
            sortino_ratio_value = sortino_ratio(selected_ticker, fecha_inicio, fecha_fin, df = nasdaq_tickers_historic, risk_free_rate=risk)
<<<<<<< HEAD
    
            
=======
>>>>>>> main
            st.write(f"**Sortino Ratio:** {sortino_ratio_value}")
            if sortino_ratio_value > 1:
                st.success('Buena inversión ajustada al riesgo')
            elif sortino_ratio_value < 1:
                st.warning('Riesgo alto en relación con el retorno')
            elif sortino_ratio_value > 2:
                st.success('Excelente inversión')
            elif sortino_ratio_value > 3:
                st.success('Inversión excepcional')

    st.write('\n')   
    st.write('\n')  
    st.write('\n')
    
    st.subheader(f"**Explicación de los ratios**")
    with st.expander(f"**Mostrar explicación**"):
        st.write(f'**ROI**: Return on Investment, es el retorno de la inversión.')
        st.write(f'**Sharpe Ratio**: Es una medida de la rentabilidad ajustada al riesgo.')
        st.write(f'**Sortino Ratio**: Es una medida de la rentabilidad ajustada al riesgo, pero solo tiene en cuenta los rendimientos negativos.')
        st.write(f'**Riesgo**: Es el riesgo personalizado para la inversión a realizar.')

