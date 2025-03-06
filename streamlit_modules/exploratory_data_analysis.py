import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

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

# Funcion pagina streamlit EDA

def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("Análisis Exploratorio de Datos")
    st.write("")
    st.header("Índice bursátil - NASDAQ 100")
    st.write("")
    st.markdown("""Bienvenido al EDA de las empresas que componen el indice bursatil de Nasdaq 100.  
    En esta sección dispones de varios tipos de análisis, métricas financieras, gráficos y visualización detallada de las tablas de datos.  
    Interactúa y utiliza los distintos selectores de ticker, período temporal, sección para configurar los análisis según tus necesidades y preferencias.
    """)
    st.write("\n")
    st.write("\n")

    # Obtener lista de tickers únicos y ordenarlos alfabéticamente
    tickers_unicos =  nasdaq_tickers_info[['Ticker', 'ShortName']]
    tickers_unicos = tickers_unicos.sort_values(by='Ticker')

    tickers_opciones = tickers_unicos.apply(lambda row: f"{row['Ticker']} - {row['ShortName']}", axis=1).tolist()

    # Selección del ticker
    st.subheader("🏢 Elige una empresa del índice por su clave Ticker")
    st.write("\n")  
    ticker_seleccionado = st.selectbox("Elige una empresa",
        tickers_opciones
    )

    # Extraer solo el ticker seleccionado (separa el texto antes del " - ")
    ticker_seleccionado = ticker_seleccionado.split(" - ")[0]

    # Obtener la información completa del ticker seleccionado
    info = nasdaq_tickers_info[nasdaq_tickers_info["Ticker"] == ticker_seleccionado]

    # Extraer los valores de las columnas
    short_name, sector, industry, country, market_cap = [
        info[col].values[0] if not info[col].empty else "No disponible"
        for col in ["ShortName", "Sector", "Industry", "Country", "MarketCap"]
    ]

    # Mostrar la información adicional en columnas
    st.write("\n")
    cols = st.columns(5)
    labels = ["Nombre", "Sector", "Industria", "País", 'MarketCap']
    values = [short_name, sector, industry, country, f'{market_cap} $M']

    for col, label, value in zip(cols, labels, values):
        with col:
            st.write(f"**{label}:** {value}")


    # Extraer solo el ticker seleccionado (separa el texto antes del " - ")
    ticker_seleccionado = ticker_seleccionado.split(" - ")[0]

    # Selección de período
    st.write("\n")
    st.subheader("📅 Selecciona el período de tiempo para el análisis.")
    st.write("\n")
    # Definimos fecha mínima y máxima para el selector de calendario
    fecha_minima = datetime(2010, 1, 1) 
    fecha_maxima = datetime.today()  

    # Selección del rango de fechas
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha de inicio", datetime(2020, 1, 1), min_value=fecha_minima, max_value=fecha_maxima)
    with col2:
        fecha_fin = st.date_input("Fecha de fin", datetime.today(), min_value=fecha_minima, max_value=fecha_maxima)

    # Convertir las fechas a datetime64[ns] para filtrar el dataframe
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Filtrar los df para el ticker seleccionado
    df_filtrado_info =  nasdaq_tickers_info[ nasdaq_tickers_info['Ticker'] == ticker_seleccionado]
    df_filtrado_historic = nasdaq_tickers_historic[nasdaq_tickers_historic['Ticker'] == ticker_seleccionado]


    # Definir las opciones del selector para la sección

    opciones_seccion = ["Selecciona una sección:","Análisis Financiero - Balance General", "Análisis Técnico - valores de cierre - SMA - RSI", "Indicadores y métricas - ROI - Sharpe - Sortino", "Tablas:  Información general -  Histórico de precios"]
    st.write("\n")
    st.write("\n")
    st.subheader("🔍Escoge una sección y empieza a explorar!")
    st.write("\n")
    seccion_seleccionada = st.selectbox("Secciones:", opciones_seccion)

    # Verificar si hay datos para el ticker seleccionado
    if not df_filtrado_info.empty and not df_filtrado_historic.empty:
        if seccion_seleccionada == "Análisis Financiero - Balance General":
            st.header("- 📊 Análisis Financiero")
            st.write("\n")
            st.markdown("""
            En esta sección podrás observar el balance general; activos, pasivos y patrimonio neto de la empresa que seleccionaste.
            """)

        
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


            # --- Gráfico del balance general ---
            st.subheader("Balance General")

            balance_general = pd.DataFrame({
                    'Concepto': ['Activos', 'Pasivos', 'Patrimonio'],
                    'Monto': [activos, pasivos, patrimonio]
                })
            fig_balance = px.bar(balance_general, x='Concepto', y='Monto', text='Monto', title=f"{ticker_seleccionado} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}")
            st.plotly_chart(fig_balance)
            st.markdown("""
            En esta grafica se muestra la relación entre activos, pasivos y patrimonio de la empresa.

            - **Activos:** Representan lo que la empresa tiene y su capacidad para generar ingresos.
            - **Pasivos:** Representan las obligaciones financieras de la empresa (la deuda a terceros).
            - **Patrimonio:** Refleja la salud financiera y el valor real de la empresa.

            Estos conceptos son clave para entender la estructura financiera y la solidez de la empresa.
            """)

            st.write("\n")

            # --- Gráfico del estado de resultados ---
            #st.subheader("Estado de Resultados")
            #estado_resultados = pd.DataFrame({
            #       'Concepto': ['Utilidad Bruta', 'Utilidad Neta'],
            #       'Monto': [u_bruta, u_neta]
            #   })
            #fig_resultados = px.bar(estado_resultados, x='Concepto', y='Monto', text='Monto', title=f"{ticker_seleccionado} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}") 
            #st.plotly_chart(fig_resultados)
            #st.markdown("""
            #Rentabilidad de la empresa en diferentes niveles brutos y netos.

            #- Rentabilidad **bruta**: Indica las ganancias después de los costes de venta (costes directos).
            #- Rentabilidad **neta**: Indica las ganancias después de deducir todos los gastos del negocio (costes directos, costes operativos e impuestos).

            #Ambas son importantes para entender la eficiencia y salud financiera del negocio.
            #""")

            st.write("\n")
            st.write("\n")
            st.write("\n")

        elif seccion_seleccionada == "Análisis Técnico - valores de cierre - SMA - RSI":
            st.write("\n")  
            st.header("- 📈 Análisis Técnico")
            st.write("\n")
            st.write("\n")
            st.markdown("""
            Aquí encontrarás gráficos más técnicos que muestran la evolución de los precios y la performance de las acciones. 
            """)
            st.write("\n")

            # --- Gráfico de análisis técnico, precios historicos---

            st.subheader("**Precios Históricos de cierre.**")
            fig_precios = px.line(df_filtrado_historic, x='Date', y='Close', title=f"{ticker_seleccionado} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}")
            st.plotly_chart(fig_precios)
            st.markdown("""
            Nos permite observar cómo ha cambiado el precio de cierre del activo a lo largo del tiempo y analizar tendencias, volatilidad y comportamiento del mercado.     

            **Contexto:**
                                
            - **Análisis técnico:** Son fundamentales para trazar líneas de tendencia, medias móviles y otros indicadores.
            - **Toma de decisiones:** Ayudan a inversores y traders a decidir cuándo comprar, vender o mantener un activo.
            - **Volatilidad:** Muestran cómo ha variado el precio en el tiempo, lo que indica el riesgo asociado al activo.   
            """)

            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")

            # --- Gráfico de análisis técnico, Medias móviles ---

            st.subheader("**Medias Móviles (SMA)**")
            df_filtrado_historic['SMA_50'] = df_filtrado_historic['Close'].rolling(window=50).mean()
            df_filtrado_historic['SMA_200'] = df_filtrado_historic['Close'].rolling(window=200).mean()

            fig_medias = go.Figure()
            fig_medias.add_trace(go.Scatter(x=df_filtrado_historic['Date'], y=df_filtrado_historic['Close'], name='Precio de Cierre'))
            fig_medias.add_trace(go.Scatter(x=df_filtrado_historic['Date'], y=df_filtrado_historic['SMA_50'], name='SMA 50', line = dict(color='green')))
            fig_medias.add_trace(go.Scatter(x=df_filtrado_historic['Date'], y=df_filtrado_historic['SMA_200'], name='SMA 200', line = dict(color='red')))
            fig_medias.update_layout(title=f"{ticker_seleccionado}")
            st.plotly_chart(fig_medias)
            st.markdown("""
            
            Las medias móviles son indicadores técnicos que suavizan los precios de un activo para identificar **tendencias** y posibles **puntos de entrada o salida**.

            **Contexto:**  
                        
            - **Media Móvil Simple (SMA):** Promedio de los precios de cierre durante un período específico.
            - **SMA 50 días:** Refleja la tendencia a corto/medio plazo.
            - **SMA 200 días:** Refleja la tendencia a largo plazo.

            ¿Estas medidas clave cómo se usan?
            - 🟢 **Cruce alcista:** Cuando la SMA de corto plazo (50 días) cruza por encima de la SMA de largo plazo (200 días), puede indicar una tendencia alcista.
            - 🔴 **Cruce bajista:** Cuando la SMA de corto plazo cruza por debajo de la SMA de largo plazo, puede indicar una tendencia bajista.
            """)

            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")  

            # --- Gráfico de analisis técnico, RSI (Relative Strength Index)---

            st.subheader("**Índice de Fuerza Relativa (RSI) 14 días**")
            def calcular_rsi(data, window=14):
                delta = data['Close'].diff()
                ganancia = (delta.where(delta > 0, 0)).rolling(window=window).mean()
                perdida = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
                rs = ganancia / perdida
                rsi = 100 - (100 / (1 + rs))
                return rsi

            df_filtrado_historic['RSI'] = calcular_rsi(df_filtrado_historic)
            fig_rsi = px.line(df_filtrado_historic, x='Date', y='RSI', title=f"{ticker_seleccionado}")
            st.plotly_chart(fig_rsi)
            st.markdown("""
            El RSI mide la fuerza del precio y puede indicar zonas de sobrecompra o sobreventa, se usa generalmente para identificar cambios de tendencia.  
            
            **Contexto:**  
                        
            - **Sobrecompra = RSI > 70 :** Cuando el RSI supera el 70, indica que el activo podría estar sobrecomprado, lo que sugiere que el precio ha subido demasiado rápido y podría estar a punto de corregirse.  
            - **Sobreventa = RSI < 30 :** Cuando el RSI cae por debajo del 30, señala que el activo podría estar en una zona de sobreventa, lo que sugiere que el precio ha caído demasiado y podría haber una oportunidad de rebote o recuperación.  
            """)
                

        elif seccion_seleccionada == "Indicadores y métricas - ROI - Sharpe - Sortino":
            st.write("\n")
            st.header("📉 Indicadores y Métricas ")
            st.write("\n")
            st.markdown("""
            Esta sección te permite interactuar con gráficos avanzados como las velas japonesas y las bandas de Bollinger.  
                         
            Estos gráficos te ayudarán a visualizar la volatilidad y la tendencia del precio de las acciones seleccionadas, además de incluir indicadores como el ROI, el Sharpe Ratio y Sortino Ratio.
            """)

            # Convertir la columna 'Date' a tipo datetime
            nasdaq_tickers_historic['Date'] = pd.to_datetime(nasdaq_tickers_historic['Date'])

            tickers_nasdaq = nasdaq_tickers_info["Ticker"].unique().tolist()

            st.write("\n")
            

            #Grafico de velas
            # Filtrar datos según el ticker y el rango de fechas
            df_filtrado = nasdaq_tickers_historic[
                (nasdaq_tickers_historic["Ticker"] == ticker_seleccionado) &
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
                        name=ticker_seleccionado
                    )
                ])

                # Personalizar el diseño
                fig.update_layout(
                    title=f" {ticker_seleccionado} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}",
                    xaxis_title="Fecha",
                    yaxis_title="Precio",
                    xaxis_rangeslider_visible=False,
                    template="plotly_dark"
                )
                st.subheader("Gráfico de Velas Japonesas")
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

            st.write("\n")  
            st.write("\n")  
            st.write("\n")
            st.write("\n")
            st.write("\n")

            #Grafico de Bandas de Bollinger
            # Filtrar datos según el ticker y el rango de fechas seleccionado
            df_ticker = nasdaq_tickers_historic[
                (nasdaq_tickers_historic["Ticker"] == ticker_seleccionado) & 
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
                fig_bollinger.update_layout(title=f" {ticker_seleccionado} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}")

                # Agregar las trazas al gráfico
                fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Close"], mode="lines", name="Precio"))
                fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["SMA"], mode="lines", name="SMA"))
                fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Upper"], mode="lines", name="Upper Band", line=dict(dash="dot")))
                fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Lower"], mode="lines", name="Lower Band", line=dict(dash="dot")))

                st.subheader("Bandas de Bollinger")
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
                La distancia entre las bandas nos muestra cuánta volatilidad hay en el mercado.  
                Bandas amplias indican más volatilidad, y más estrechas menos.
                """)


            st.write("\n")
            st.write("\n")
            st.write("\n")  
            st.write("\n")  
            st.write("\n")

            st.subheader("📊 Métricas")

            st.write("\n")
            st.write("\n")
            st.write("\n")
            # Estructura ROI + Input de Riesgo
            col_roi, col_risk = st.columns([2, 1]) 
            with col_roi:
                roi_value = roi(ticker_seleccionado, fecha_inicio, fecha_fin, df=nasdaq_tickers_historic)
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
                sharpe_value = sharpe_ratio(ticker_seleccionado, fecha_inicio, fecha_fin, df=nasdaq_tickers_historic, risk_free_rate=risk)
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
                sortino_ratio_value = sortino_ratio(ticker_seleccionado, fecha_inicio, fecha_fin, df=nasdaq_tickers_historic, risk_free_rate=risk)
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
            st.write("\n")
            st.write("\n")  

            # Explicación de los ratios
            st.markdown("""
            **Explicación de los ratios:**  
            - **ROI**: Retorno de la inversión, mide el beneficio generado en relación con la inversión inicial.  
            - **Sharpe Ratio**: Rentabilidad ajustada al riesgo considerando la volatilidad total.  
            - **Sortino Ratio**: Similar al Sharpe Ratio, pero solo tiene en cuenta la volatilidad negativa (riesgo a la baja).  
            - **Riesgo personalizado**: Parámetro ajustable para analizar inversiones según tu tolerancia al riesgo.
            """)

        elif seccion_seleccionada == "Tablas:  Información general -  Histórico de precios":    
            st.header("- 📋 Tablas de Datos")
            st.write("\n")
            st.markdown("""
            Aquí podrás acceder a las tablas de datos históricos y financieros que se han utilizado para generar los gráficos y análisis anteriores. 
            Consulta los valores crudos de precios, volumen, activos, pasivos y más. 
            Las tablas están organizadas para facilitar la visualización y exportación de los datos si lo necesitas.
            """)
            st.write("")
            
            # Para nasdaq_tickers_info:
            if nasdaq_tickers_info.index.name == 'Ticker' or 'Ticker' not in nasdaq_tickers_info.columns:
                nasdaq_tickers_info = nasdaq_tickers_info.reset_index()
            if 'Ticker' in nasdaq_tickers_info.columns:
                cols = ['Ticker'] + [col for col in nasdaq_tickers_info.columns if col != 'Ticker']
                nasdaq_tickers_info = nasdaq_tickers_info[cols]
            
            # Ajustar el índice para que empiece en 1
            nasdaq_tickers_info.index = nasdaq_tickers_info.index + 1
            
            st.subheader("- Información general de las empresas integrantes del índice Nasdaq-100")
            st.write("\n")
            st.write("\n")
            st.dataframe(nasdaq_tickers_info)
            
            st.write("\n")
            st.write("📖 Glosario de términos financieros de la tabla de información general:")
            st.write("\n")
            with st.expander("Despliega para entender los términos de la tabla"):
                st.markdown("""
                    - **Ticker:** Símbolo de cotización de una empresa en la bolsa.  
                    - **ShortName:** Nombre corto o abreviado de la empresa.  
                    - **Sector:** Categoría general de la industria a la que pertenece la empresa.  
                    - **Industry:** Industria específica dentro del sector en el que opera la empresa.  
                    - **Country:** País en el que está registrada la empresa.  
                    - **ReturnOnAssets (ROA):** Rentabilidad sobre activos, mide la eficiencia en el uso de activos para generar ganancias.  
                    - **ReturnOnEquity (ROE):** Rentabilidad sobre el patrimonio, indica cuánto beneficio genera la empresa en relación con su capital propio.  
                    - **OperatingMargins:** Margen operativo, mide la rentabilidad después de costos operativos pero antes de intereses e impuestos.  
                    - **GrossMargins:** Margen bruto, porcentaje de ingresos que queda después de costos de producción.  
                    - **ProfitMargins:** Margen de beneficio neto, porcentaje de ingresos que queda como ganancia después de todos los gastos.  
                    - **ebitdaMargins:** Margen EBITDA, mide la rentabilidad antes de intereses, impuestos, depreciación y amortización.  
                    - **MarketCap:** Capitalización bursátil, valor total de las acciones en circulación de una empresa.  
                    - **TotalRevenue:** Ingresos totales, dinero generado por la empresa en un periodo determinado.  
                    - **NetIncomeToCommon:** Beneficio neto atribuible a los accionistas comunes, ganancias después de todos los gastos e impuestos.  
                    - **DebtToEquity:** Relación deuda-capital, mide cuánto financiamiento proviene de deuda en comparación con el capital propio.  
                    - **FreeCashflow:** Flujo de caja libre, dinero disponible después de gastos operativos y de capital.  
                    - **DividendRate:** Tasa de dividendo, cantidad de dividendos pagados por acción en un periodo.  
                    - **DividendYield:** Rentabilidad por dividendo, porcentaje del dividendo anual en relación con el precio de la acción.  
                    - **PayoutRatio:** Ratio de pago, porcentaje de las ganancias que la empresa distribuye en dividendos.""")

            st.write("\n")
            st.write("\n")  
            st.write("\n")  
            st.write("\n")  
            
            # Para nasdaq_tickers_historic:
            if nasdaq_tickers_historic.index.name == 'Ticker' or 'Ticker' not in nasdaq_tickers_historic.columns:
                nasdaq_tickers_historic = nasdaq_tickers_historic.reset_index()
            if 'Ticker' in nasdaq_tickers_historic.columns:
                cols = ['Ticker'] + [col for col in nasdaq_tickers_historic.columns if col != 'Ticker']
                nasdaq_tickers_historic = nasdaq_tickers_historic[cols]

            
            
            # Ajustar el índice para que empiece en 1
            nasdaq_tickers_historic.index = nasdaq_tickers_historic.index + 1
            
            st.subheader("- Precios históricos de las empresas integrantes del índice Nasdaq-100")
            st.write("\n")
            st.write("\n")
            st.dataframe(nasdaq_tickers_historic)
            
            st.write("\n")
            st.write("📖 Glosario de términos de precios históricos del mercado bursátil")

            with st.expander("Despliega para entender los términos de la tabla"):
                st.markdown("""
                - **Ticker:** Símbolo de cotización de una empresa en la bolsa.    
                - **Date:** Fecha específica del registro de los datos.  
                - **Close:** Precio de cierre de la acción en la sesión de mercado.  
                - **High:** Precio más alto alcanzado por la acción en la sesión.  
                - **Low:** Precio más bajo alcanzado por la acción en la sesión.  
                - **Open:** Precio al que abrió la acción en la sesión de mercado.  
                - **Volume:** Número total de acciones negociadas en la sesión.  
                """)


    else:
    # Si no hay datos para el ticker seleccionado
        st.warning("No hay datos disponibles para el ticker seleccionado.")
        
