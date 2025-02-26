import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
#from descarga_sql import nasdaq_tickers_historic, nasdaq_tickers_info

def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    
    # Título del dashboard
    st.title("Dashboard de Análisis Financiero y Técnico - Nasdaq 100")

    # Obtener lista de tickers únicos y ordenarlos alfabéticamente
    tickers_unicos =  nasdaq_tickers_info[['Ticker', 'ShortName']]
    tickers_unicos = tickers_unicos.sort_values(by='Ticker')

    tickers_opciones = tickers_unicos.apply(lambda row: f"{row['Ticker']} - {row['ShortName']}", axis=1).tolist()


    # Selección del ticker
    ticker_seleccionado = st.selectbox(
        "Selecciona un Ticker",
        tickers_opciones
    )

    # Extraer solo el ticker seleccionado (separa el texto antes del " - ")
    ticker_seleccionado = ticker_seleccionado.split(" - ")[0]

    # Filtrar el dataframe de información para el ticker seleccionado
    df_filtrado_info =  nasdaq_tickers_info[ nasdaq_tickers_info['Ticker'] == ticker_seleccionado]

    # Filtrar el dataframe histórico para el ticker seleccionado
    df_filtrado_historic = nasdaq_tickers_historic[nasdaq_tickers_historic['Ticker'] == ticker_seleccionado]

    # Verificar si hay datos para el ticker seleccionado
    if not df_filtrado_info.empty and not df_filtrado_historic.empty:
        # --- Cálculos para el balance general y estado de resultados ---
        net_income = df_filtrado_info['NetIncomeToCommon'].values[0]
        roe = df_filtrado_info['ReturnOnEquity'].values[0]
        debt_to_equity = df_filtrado_info['DebtToEquity'].values[0]
        total_revenue = df_filtrado_info['TotalRevenue'].values[0]
        gross_margins = df_filtrado_info['GrossMargins'].values[0]

        patrimonio = net_income / roe 
        pasivos = debt_to_equity * patrimonio
        activos = pasivos + patrimonio

        coste_bienes_vendidos = total_revenue * (1 - gross_margins)
        u_bruta = total_revenue - coste_bienes_vendidos
        u_neta = net_income / 1_000_000

        # --- Gráficos del balance general y estado de resultados ---
        st.subheader("Análisis Financiero")

        #st.markdown("**Balance General**")
        balance_general = pd.DataFrame({
                'Concepto': ['Activos', 'Pasivos', 'Patrimonio'],
                'Monto': [activos, pasivos, patrimonio]
            })
        fig_balance = px.bar(balance_general, x='Concepto', y='Monto', text='Monto', title=f"Balance general de la empresa {ticker_seleccionado}")
        st.plotly_chart(fig_balance)
        st.markdown("""
📌 Relación entre <strong>activos, pasivos y patrimonio</strong> de la empresa.

- 🔋 <strong>Activos</strong>: Representan lo que la empresa tiene y su capacidad para generar ingresos.
- 🪫 <strong>Pasivos</strong>: Representan las obligaciones financieras de la empresa (la deuda a terceros).
- 💶 <strong>Patrimonio</strong>: Refleja la salud financiera y el valor real de la empresa.

<p style="font-weight: normal;">🧮 Estos conceptos son clave para entender la estructura financiera y la solidez de la empresa.</p>
---
""", unsafe_allow_html=True)

        #st.markdown("**Estado de Resultados**")
        estado_resultados = pd.DataFrame({
                'Concepto': ['Utilidad Bruta', 'Utilidad Neta'],
                'Monto': [u_bruta, u_neta]
            })
        fig_resultados = px.bar(estado_resultados, x='Concepto', y='Monto', text='Monto', title=f"Estado de resultados de la empresa {ticker_seleccionado}")
        st.plotly_chart(fig_resultados)
        st.markdown("""
📌 **Rentabilidad** de la empresa en diferentes niveles brutos y netos.

- Rentabilidad **bruta**: Indica las ganancias después de los costes de venta (costes directos).
- Rentabilidad **neta**: Indica las ganancias después de deducir todos los gastos del negocio (costes directos, costes operativos e impuestos).

💰 Ambas son importantes para entender la eficiencia y salud financiera del negocio.
""")

        # --- Gráficos de análisis técnico ---
        st.subheader("Análisis Técnico")

        # Precios históricos
        st.markdown("**Precios Históricos**")
        fig_precios = px.line(df_filtrado_historic, x='Date', y='Close', title=f"Precios de Cierre para {ticker_seleccionado}")
        st.plotly_chart(fig_precios)
        st.markdown("""
📌 Evolución de los **precios de cierre** del activo seleccionado.

💹 Refleja cómo ha cambiado el precio de cierre del activo a lo largo del tiempo.
🔎 Permite analizar tendencias, volatilidad y comportamiento del mercado.     

Importancia:
                    
- 📈 Análisis técnico: Son fundamentales para trazar líneas de tendencia, medias móviles y otros indicadores.
- ☑️ Toma de decisiones: Ayudan a inversores y traders a decidir cuándo comprar, vender o mantener un activo.
- 📉 Volatilidad: Muestran cómo ha variado el precio en el tiempo, lo que indica el riesgo asociado al activo.   
                    
 ---""")

        # Medias móviles
        st.markdown("**Medias Móviles (SMA)**")
        df_filtrado_historic['SMA_50'] = df_filtrado_historic['Close'].rolling(window=50).mean()
        df_filtrado_historic['SMA_200'] = df_filtrado_historic['Close'].rolling(window=200).mean()

        fig_medias = go.Figure()
        fig_medias.add_trace(go.Scatter(x=df_filtrado_historic['Date'], y=df_filtrado_historic['Close'], name='Precio de Cierre'))
        fig_medias.add_trace(go.Scatter(x=df_filtrado_historic['Date'], y=df_filtrado_historic['SMA_50'], name='SMA 50', line = dict(color='green')))
        fig_medias.add_trace(go.Scatter(x=df_filtrado_historic['Date'], y=df_filtrado_historic['SMA_200'], name='SMA 200', line = dict(color='red')))
        fig_medias.update_layout(title=f"Medias Móviles para {ticker_seleccionado}")
        st.plotly_chart(fig_medias)
        st.markdown(""" 📌 **Las medias móviles** son indicadores técnicos que suavizan los precios de un activo para identificar **tendencias** y posibles **puntos de entrada o salida**.

    🔹 Conceptos Clave:
    - 📈 **Media Móvil Simple (SMA):** Promedio de los precios de cierre durante un período específico.
    - 📉 **SMA 50 días:** Refleja la tendencia a corto/medio plazo.
    - 📊 **SMA 200 días:** Refleja la tendencia a largo plazo.

    🔹 ¿Cómo se usan?
    - 🟢 **Cruce alcista:** Cuando la SMA de corto plazo (50 días) cruza por encima de la SMA de largo plazo (200 días), puede indicar una tendencia alcista.
    - 🔴 **Cruce bajista:** Cuando la SMA de corto plazo cruza por debajo de la SMA de largo plazo, puede indicar una tendencia bajista.

    ---""")

        # RSI (Relative Strength Index)
        st.markdown("**Índice de Fuerza Relativa (RSI)**")
        def calcular_rsi(data, window=14):
            delta = data['Close'].diff()
            ganancia = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            perdida = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = ganancia / perdida
            rsi = 100 - (100 / (1 + rs))
            return rsi

        df_filtrado_historic['RSI'] = calcular_rsi(df_filtrado_historic)
        fig_rsi = px.line(df_filtrado_historic, x='Date', y='RSI', title=f"RSI (14 días) para {ticker_seleccionado}")
        st.plotly_chart(fig_rsi)
        st.markdown("""
    📌 **El RSI** mide la fuerza del precio y puede indicar zonas de **sobrecompra o sobreventa**.

    - 🔴 **Sobrecompra:** RSI > 70
    - 🟢 **Sobreventa:** RSI < 30
    - 📊 Generalmente, se usa para identificar cambios de tendencia.
    """)

    else:
        st.warning("No hay datos disponibles para el ticker seleccionado.")