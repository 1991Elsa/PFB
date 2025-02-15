
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
from tickers_nasdaq import tickers_nasdaq
from data_cleaning import clean_data



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
        fecha_inicio = st.date_input("Selecciona la fecha de inicio", pd.to_datetime("2020-01-01"))
    with col5:
        fecha_fin = st.date_input("Selecciona la fecha de fin", pd.Timestamp.now()) 



    #Para pagina 2
    tickers_nasdaq_no_ndx = tickers_nasdaq()
    tickers_nasdaq_no_ndx.remove('NDX')
 

    selected_ticker = st.selectbox("Selecciona el número de tickers a mostrar", options = tickers_nasdaq_no_ndx)
    info = nasdaq_tickers_info[nasdaq_tickers_info["Ticker"] == selected_ticker]
    short_name, sector, industry, country = [
        info[col].values[0] if not info[col].empty else "No disponible"
        for col in ["ShortName", "Sector", "Industry", "Country"]
    ]

    
    cols = st.columns(4)
    labels = ["Nombre corto", "Sector", "Industria", "País"]
    values = [short_name, sector, industry, country]

    for col, label, value in zip(cols, labels, values):
        with col:
            st.write(f"**{label}:** {value}")

    
if __name__ == "__main__":  
    main() 