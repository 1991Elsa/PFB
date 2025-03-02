import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
#from descarga_sql import descargar_data_sql

#nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

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

def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("Dashboard Interactivo")
    st.write("Este es el contenido del Dashboard Interactivo.")

    # Cargar datos desde archivo CSV
    #nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

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
    st.subheader("📅 Selecciona el período de tiempo para el análisis.")
    st.write("")

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

    #Grafico de velas
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

        st.markdown("""
        **Interpretacion:** 

        Las velas japonesas muestran la variación del precio de un activo en un periodo de tiempo.

        Cada vela tiene:
        - **Apertura (Open)**: El precio al inicio del periodo.
        - **Cierre (Close)**: El precio al final del periodo.
        - **Máximo (High)**: El precio más alto durante el periodo.
        - **Mínimo (Low)**: El precio más bajo durante el periodo.
                    
        **¿Qué nos indican las velas?**
        Cuando el precio de cierre es mayor que el de apertura, la vela es **verde** indicando que el precio subió.
        Cuando el precio de cierre es menor que el de apertura, la vela es **roja** indicando que el precio bajó.
        Con este gráfico puedes ver la tendencia y la volatilidad del precio del activo.
        """)


    #Grafico de Bandas de Bollinger
    # Filtrar datos según el ticker y el rango de fechas seleccionado
    df_ticker = nasdaq_tickers_historic[
        (nasdaq_tickers_historic["Ticker"] == selected_ticker) & 
        (nasdaq_tickers_historic["Date"] >= fecha_inicio) & 
        (nasdaq_tickers_historic["Date"] <= fecha_fin)
    ].copy()

    # Verificar si hay datos disponibles después del filtrado
    if df_ticker.empty:
        st.warning("No hay datos disponibles para el rango seleccionado.")
    else:
        # Calcular las Bandas de Bollinger sobre los datos filtrados
        df_ticker["SMA"] = df_ticker["Close"].rolling(20).mean()
        df_ticker["Upper"] = df_ticker["SMA"] + 2 * df_ticker["Close"].rolling(20).std()
        df_ticker["Lower"] = df_ticker["SMA"] - 2 * df_ticker["Close"].rolling(20).std()

        # Crear el gráfico de las Bandas de Bollinger
        fig_bollinger = go.Figure()

        # Título dinámico con el rango de fechas seleccionado
        fig_bollinger.update_layout(title=f"Bandas de Bollinger - {selected_ticker} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}")

        # Agregar las trazas al gráfico
        fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Close"], mode="lines", name="Precio"))
        fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["SMA"], mode="lines", name="SMA"))
        fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Upper"], mode="lines", name="Upper Band", line=dict(dash="dot")))
        fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Lower"], mode="lines", name="Lower Band", line=dict(dash="dot")))

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_bollinger)

    st.markdown("""
        **Interpretacion:** 
                       
        Las Bandas de Bollinger ayudan a medir la volatilidad del precio de un activo.

        - **Precio**: Muestra el valor del activo en cada momento.
        - **SMA**: Es el promedio de los precios durante los últimos 20 días, que ayuda a identificar la tendencia general.
        - **Upper Band**: Está dos desviaciones estándar por encima de la SMA, señalando un posible nivel de sobrecompra.
        - **Lower Band**: Está dos desviaciones estándar por debajo de la SMA, indicando un posible nivel de sobreventa.

        **¿Qué nos indican las bandas?**
         La distancia entre las bandas nos muestra cuánta volatilidad hay en el mercado. Bandas amplias indican más volatilidad, y más estrechas menos.
        """)

    
    st.subheader("📊 Métricas")

    # Estructura ROI + Input de Riesgo
    col_roi, col_risk = st.columns([2, 1]) 
    with col_roi:
        roi_value = roi(selected_ticker, fecha_inicio, fecha_fin, df=nasdaq_tickers_historic)
        st.write("**ROI:**")
        if roi_value > 0:
            st.success(f'📈 Invertir en esta acción habría generado una ganancia del {roi_value:.2f}%')
        elif roi_value < 0:
            st.error(f'📉 Si hubieras invertido en esta acción, habrías perdido un {roi_value:.2f}% de tu inversión.')
        else:
            st.info(f'🔍 La inversión no generó ganancias ni pérdidas ({roi_value:.2f}%)')

    with col_risk:
        risk = st.number_input("📉 Introducee el riesgo personalizado (%)", min_value=0.0, max_value=100.0, value=20.00, step=0.01)
        risk = risk / 100  

    st.write("\n")  

    # Estructura Sharpe y Sortino Ratio
    col_sharpe, col_sortino = st.columns(2)

    with col_sharpe:
        sharpe_value = sharpe_ratio(selected_ticker, fecha_inicio, fecha_fin, df=nasdaq_tickers_historic, risk_free_rate=risk)
        st.write(f"**Sharpe Ratio:** {sharpe_value:.2f}")
        if sharpe_value > 3:
            st.success('🚀 Inversión excepcional')
        elif sharpe_value > 2:
            st.success('✅ Excelente inversión')
        elif sharpe_value > 1:
            st.success('Buena inversión ajustada al riesgo')
        else:
            st.warning('⚠️ Riesgo alto en relación con el retorno')

    with col_sortino:
        sortino_ratio_value = sortino_ratio(selected_ticker, fecha_inicio, fecha_fin, df=nasdaq_tickers_historic, risk_free_rate=risk)
        st.write(f"**Sortino Ratio:** {sortino_ratio_value:.2f}")
        if sortino_ratio_value > 3:
            st.success('🚀 Inversión excepcional')
        elif sortino_ratio_value > 2:
            st.success('✅ Excelente inversión')
        elif sortino_ratio_value > 1:
            st.success('Buena inversión ajustada al riesgo')
        else:
            st.warning('⚠️ Riesgo alto en relación con el retorno')

    st.write("\n")

    # Explicación de los ratios
    st.markdown("""
    **Explicación de los ratios:**  
    - **ROI**: Retorno de la inversión, mide el beneficio generado en relación con la inversión inicial.  
    - **Sharpe Ratio**: Rentabilidad ajustada al riesgo considerando la volatilidad total.  
    - **Sortino Ratio**: Similar al Sharpe Ratio, pero solo tiene en cuenta la volatilidad negativa (riesgo a la baja).  
    - **Riesgo personalizado**: Parámetro ajustable para analizar inversiones según tu tolerancia al riesgo.
    """)
