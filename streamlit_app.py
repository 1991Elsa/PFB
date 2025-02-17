
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
from tickers_nasdaq import tickers_nasdaq
from data_cleaning import clean_data
from roi import roi
from func_sharpe_sortino import sharpe_ratio, sortino_ratio


def get_datos_historicos(tickers, start_date="2020-01-01"):
    end_date = datetime.now().strftime('%Y-%m-%d')
    datos = yf.download(tickers, start=start_date, end=end_date, progress=False, group_by="ticker")
    if isinstance(datos.columns, pd.MultiIndex):
        datos.columns = ['_'.join(col).strip() for col in datos.columns]
    datos = datos.copy()
    datos.reset_index(inplace=True)
    datos = datos.melt(id_vars=['Date'], var_name="Variable", value_name="Valor")
    datos[['Ticker', 'Metric']] = datos['Variable'].str.rsplit('_', n=1, expand=True)
    datos = datos.pivot(index=['Date', 'Ticker'], columns='Metric', values='Valor').reset_index()
    return datos

def get_ticker_info(ticker):
    ticker_info = yf.Ticker(ticker).info
    return ticker_info

# Obtener la lista de tickers del NASDAQ
tickers = tickers_nasdaq()

# Obtener los datos históricos de todos los tickers del NASDAQ
nasdaq_tickers_historic = get_datos_historicos(tickers)

# Inicializar un DataFrame para almacenar la información de los tickers
nasdaq_tickers_info = pd.DataFrame()

# Obtener la información de cada ticker individualmente y almacenarla
def obtener_informacion_tickers(tickers):
    nasdaq_tickers_info = pd.DataFrame()
    for ticker in tickers:
        if ticker != 'NDX':
            ticker_info = get_ticker_info(ticker)
            dic_info = {
                'Ticker': ticker_info.get('symbol', ticker), 
                'ShortName': ticker_info.get('shortName', 'N/A'), 
                'Sector': ticker_info.get('sector', 'N/A'),
                'Industry': ticker_info.get('industry', 'N/A'),
                'Country': ticker_info.get('country', 'N/A'),
                'FullTimeEmployees': ticker_info.get('fullTimeEmployees', 'N/A'),
                'MarketCap': ticker_info.get('marketCap', 'N/A'), 
                'TotalRevenue': ticker_info.get('totalRevenue', 'N/A'), 
                'NetIncomeToCommon': ticker_info.get('netIncomeToCommon', 'N/A'),
                'TrailingEPS': ticker_info.get('trailingEps', 'N/A'),
                'ForwardEPS': ticker_info.get('forwardEps', 'N/A'),
                'TrailingPE': ticker_info.get('trailingPE', 'N/A'),
                'ForwardPE': ticker_info.get('forwardPE', 'N/A'),
                'ReturnOnAssets': ticker_info.get('returnOnAssets', 'N/A'), 
                'ReturnOnEquity': ticker_info.get('returnOnEquity', 'N/A'), 
                'DebtToEquity': ticker_info.get('debtToEquity', 'N/A'), 
                'FreeCashflow': ticker_info.get('freeCashflow', 'N/A'), 
                'DividendRate': ticker_info.get('dividendRate', 'N/A'), 
                'DividendYield': ticker_info.get('dividendYield', 'N/A'),
                'PayoutRatio': ticker_info.get('payoutRatio', 'N/A'), 
                'Beta': ticker_info.get('beta', 'N/A'), 
                'GrossMargins': ticker_info.get('grossMargins', 'N/A'), 
                'OperatingMargins': ticker_info.get('operatingMargins', 'N/A'), 
                'ProfitMargins': ticker_info.get('profitMargins', 'N/A'),
                'ebitdaMargins': ticker_info.get('ebitdaMargins', 'N/A'), 
                'Timestamp_extraction': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            df_info = pd.DataFrame([dic_info])
            nasdaq_tickers_info = pd.concat([nasdaq_tickers_info, df_info], ignore_index=True)
    return nasdaq_tickers_info

# Corrección: Llamada a la nueva función obtener_informacion_tickers
nasdaq_tickers_info = obtener_informacion_tickers(tickers)

# Limpiar los DataFrames
df_nasdaq_tickers_info_clean = clean_data(nasdaq_tickers_info)
df_nasdaq_tickers_historic_clean = clean_data(nasdaq_tickers_historic)










###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################








import streamlit as st
import pandas as pd
import yfinance as yf   
from PIL import Image
import plotly.graph_objects as go
import mplfinance as mpf
from modules.pfb_page_config_dict import PAGE_CONFIG
#from funcion_extraccion_info_historicos import *



st.set_page_config(**PAGE_CONFIG) 

#info_tickers = nasdaq_tickers_info

def main():
    st.title("PFB Yahoo Finance")
    st.write("Bienvenidos a la demo del PFB de Yahoo Finance")
    

    st.sidebar.title("Navegación")
    
    st.sidebar.success(f'Last update: \n\n{nasdaq_tickers_info["Timestamp_extraction"][1]}')

    col1, col2, col3, col4, col5 = st.columns(5) 
    with col4:
        fecha_inicio = st.date_input("Selecciona la fecha de inicio", pd.to_datetime(min(nasdaq_tickers_historic["Date"])))
    with col5:
        fecha_fin = st.date_input("Selecciona la fecha de fin", pd.to_datetime(max(nasdaq_tickers_historic["Date"])))



    #Para pagina 2
    tickers_nasdaq_no_ndx = tickers_nasdaq()
    tickers_nasdaq_no_ndx.remove('NDX')
 

    selected_ticker = st.selectbox("Selecciona el ticker a mostrar", options = tickers_nasdaq_no_ndx)
    info = nasdaq_tickers_info[nasdaq_tickers_info["Ticker"] == selected_ticker]
    short_name, sector, industry, country, MarketCap = [
        info[col].values[0] if not info[col].empty else "No disponible"
        for col in ["ShortName", "Sector", "Industry", "Country", "MarketCap"]
    ]

    
    cols = st.columns(5)
    labels = ["Nombre", "Sector", "Industria", "País", 'MarketCap']
    values = [short_name, sector, industry, country, f'{MarketCap / 1_000_000:,.0f} $M'
]

    for col, label, value in zip(cols, labels, values):
        with col:
            st.write(f"**{label}:** {value}")

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



    #Mostrar la evolucion los ultimos dias
    nasdaq_tickers_historic["Date"] = pd.to_datetime(nasdaq_tickers_historic["Date"])
    ultima_fecha = nasdaq_tickers_historic["Date"].max()

    fecha_hace_1_dia= ultima_fecha - pd.Timedelta(days=1)
    fecha_hace_7_dias = ultima_fecha - pd.Timedelta(days=7)
    fecha_hace_1_mes = ultima_fecha - pd.Timedelta(days=30)
    fecha_hace_1_anyo = ultima_fecha - pd.Timedelta(days=365)


    df_ticker = nasdaq_tickers_historic[nasdaq_tickers_historic["Ticker"] == selected_ticker]
    precio_fin = df_ticker[df_ticker["Date"] == ultima_fecha]["Close"].values
    precio_1_dia = df_ticker[df_ticker["Date"] == fecha_hace_1_dia]["Close"].values
    precio_7_dias = df_ticker[df_ticker["Date"] == fecha_hace_7_dias]["Close"].values
    precio_1_mes = df_ticker[df_ticker["Date"] == fecha_hace_1_mes]["Close"].values
    precio_1_anyo= df_ticker[df_ticker["Date"] == fecha_hace_1_anyo]["Close"].values
    

    variacion_1_dia = ((precio_fin - precio_1_dia) / precio_1_dia) * 100
    variacion_7_dias = ((precio_fin - precio_7_dias) / precio_7_dias) * 100
    variacion_1_mes = ((precio_fin - precio_1_mes) / precio_1_mes) * 100
    variacion_1_anyo = ((precio_fin - precio_1_anyo) / precio_1_anyo) * 100

    st.subheader("Evolución de los últimos días")
    evo_col1, evo_col2, evo_col3, evo_col4, evo_col5, evo_col6 = st.columns(6)
    with evo_col1:
        st.write(f"24h: {variacion_1_dia[0]:.2f} %")
    
    with evo_col2:
        st.write(f"7 dias: {variacion_7_dias[0]:.2f} %")

    with evo_col3:
        st.write(f"30 dias: {variacion_1_mes[0]:.2f} %")

    with evo_col4:
        st.write(f"1 año: {variacion_1_anyo[0]:.2f} %")


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