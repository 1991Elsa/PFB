import streamlit as st
import pandas as pd
import yfinance as yf   
from PIL import Image
import plotly.graph_objects as go
import mplfinance as mpf
from modules.pfb_page_config_dict import PAGE_CONFIG
from funciones_economicas import *
from connect_engine import get_engine_database
#from descarga_sql import descargar_data_sql



st.set_page_config(**PAGE_CONFIG) 
#nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()


nasdaq_tickers_info = pd.read_csv("nasdaq_tickers_info_clean.csv")
nasdaq_tickers_historic = pd.read_csv("nasdaq_tickers_historic_clean.csv")

def main():

    st.image(Image.open("sources/logo_ndq.jpeg"),width=50)
    
    st.title("NASDAQ 100")
    
    st.write("En esta aplicación podrás visualizar la información de los tickers del NASDAQ 100, así como su evolución en el tiempo y algunas métricas financieras.")
        
    

    st.sidebar.title("Navegación")
    
    st.sidebar.success(f'Last update: \n\n{nasdaq_tickers_info["Timestamp_extraction"][1]}')

    col1, col2, col3, col4, col5 = st.columns(5) 
    with col4:
        fecha_inicio = st.date_input("Selecciona la fecha de inicio", pd.to_datetime(min(nasdaq_tickers_historic["Date"])))
    with col5:
        fecha_fin = st.date_input("Selecciona la fecha de fin", pd.to_datetime(max(nasdaq_tickers_historic["Date"])))



    #Para pagina 2

    tickers_nasdaq = nasdaq_tickers_info["Ticker"].unique().tolist()
    #tickers_nasdaq_no_ndx = tickers_nasdaq
    #tickers_nasdaq_no_ndx.remove('NDX')
 

    selected_ticker = st.selectbox("Selecciona el ticker a mostrar", options = tickers_nasdaq)
    info = nasdaq_tickers_info[nasdaq_tickers_info["Ticker"] == selected_ticker]
    short_name, sector, industry, country, MarketCap = [
        info[col].values[0] if not info[col].empty else "No disponible"
        for col in ["ShortName", "Sector", "Industry", "Country", "MarketCap"]
    ]








    def calcular_variaciones(df, ticker):
        df["Date"] = pd.to_datetime(df["Date"])
        ultima_fecha = df["Date"].max()
        
        fechas = {
            "24h": ultima_fecha - pd.Timedelta(days=1),
            "7 días": ultima_fecha - pd.Timedelta(days=7),
            #"1 mes": ultima_fecha - pd.Timedelta(days=31),
            "1 año": ultima_fecha - pd.Timedelta(days=365)
        }
        
        df_ticker = df[df["Ticker"] == ticker]
        precio_fin = df_ticker[df_ticker["Date"] == ultima_fecha]["Close"].values
        
        variaciones = {}
        for periodo, fecha in fechas.items():
            precio_ant = df_ticker[df_ticker["Date"] == fecha]["Close"].values
            if precio_ant.size > 0 and precio_fin.size > 0:
                variaciones[periodo] = ((precio_fin[0] - precio_ant[0]) / precio_ant[0]) * 100
            else:
                variaciones[periodo] = None
        
        return variaciones

    def mostrar_variaciones(variaciones):
        st.subheader("Evolución de los últimos días")
        cols = st.columns(len(variaciones))
        
        for col, (periodo, variacion) in zip(cols, variaciones.items()):
            with col:
                if variacion is not None:
                    if variacion > 0:
                        st.success(f"{periodo}: {variacion:.2f} %")
                    elif variacion < 0:
                        st.error(f"{periodo}: {variacion:.2f} %")
                    else:
                        st.warning(f"{periodo}: {variacion:.2f} %")
                else:
                    st.warning(f"{periodo}: No disponible")


    variaciones = calcular_variaciones(nasdaq_tickers_historic, selected_ticker)
    mostrar_variaciones(variaciones)








    
    cols = st.columns(5)
    labels = ["Nombre", "Sector", "Industria", "País", 'MarketCap']
    values = [short_name, sector, industry, country, f'{MarketCap / 1_000_000:,.0f} $M']

    for col, label, value in zip(cols, labels, values):
        with col:
            st.write(f"**{label}:** {value}")

    st.write('\n')
    st.write('\n')


    #Mostrar la evolucion los ultimos dias
    

    st.write('\n')

    # Convertir fechas seleccionadas a formato compatible con el DataFrame
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
    fig_bollinger.update_layout(title=f"Bollinger Bands - {selected_ticker} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}")
    title = f"Bandas de Bollinger - {selected_ticker} de {fecha_inicio.strftime('%d-%m-%Y')} a {fecha_fin.strftime('%d-%m-%Y')}"
    fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Close"], mode="lines", name="Precio"))
    fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["SMA"], mode="lines", name="SMA"))
    fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Upper"], mode="lines", name="Upper Band", line=dict(dash="dot")))
    fig_bollinger.add_trace(go.Scatter(x=df_ticker["Date"], y=df_ticker["Lower"], mode="lines", name="Lower Band", line=dict(dash="dot")))
    st.plotly_chart(fig_bollinger)

    


    st.write('\n')
    st.write('\n')

    with st.expander("Mostrar metricas", expanded=False):
        # Calcular el ROI
        roi_value = roi(selected_ticker, fecha_inicio, fecha_fin, df = nasdaq_tickers_historic)
        st.write(f"**ROI:**")
        if roi_value > 0:
            st.success(f'Invertir en esa acción durante ese período habría generado una ganancia del {roi_value}%')
        elif roi_value < 0:
            st.error(f'Si hubieras invertido en esa acción, habrías perdido un {roi_value}% de tu inversión.')
        st.write('\n')

        #calcular sharpe ratio
        col_risk1, col_risk2, col_risk3, col_risk4, col_risk5 = st.columns(5)
        with col_risk5:
            risk= st.number_input("Introducir riesgo personalizado (%)", min_value=0.0, max_value=100.0, value=20.00, step=0.01)
            risk = risk / 100

        col_sortino, col_sharpe = st.columns(2)

        with col_sharpe:
            sharpe_value = sharpe_ratio(selected_ticker, fecha_inicio, fecha_fin, df = nasdaq_tickers_historic, risk_free_rate=risk)
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
        st.subheader(f"**Explicacion de los ratios**")
        st.write(f'**ROI**: Return on Investment, es el retorno de la inversión.')
        st.write(f'**Sharpe Ratio**: Es una medida de la rentabilidad ajustada al riesgo.')
        st.write(f'**Sortino Ratio**: Es una medida de la rentabilidad ajustada al riesgo, pero solo tiene en cuenta los rendimientos negativos.')
        st.write('Riesgo: Es el riesgo personalizado para la inversión a realizar.')

          

        
    
if __name__ == "__main__":  
    main() 