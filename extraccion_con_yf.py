import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
import time
from connect_engine import *
from tablas_metadata_5 import *
from sqlalchemy.dialects.mysql import insert

# Función para obtener los tickers de NASDAQ 100 (scrapping)
def tickers_nasdaq():
    """
Extrae mediante scrapping en la pagina TradingView los tickers de NASDAQ 100 actualizados.

Parámetros:
- No tiene.

Retorna:
- Una lista con los tickers de NASDAQ 100.
"""

    
     
    url = 'https://es.tradingview.com/symbols/NASDAQ-NDX/components/'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')


    tickers = []
    tickers.append('NDX')
    for row in soup.find_all('tr', {'class': 'row-RdUXZpkv'}):
        data_row = row.get('data-rowkey', '')
        if data_row.startswith('NASDAQ:'):
            tickers.append(data_row.replace('NASDAQ:', ''))
    print('Tickers scrapeados con exito')
    return tickers


# Función para obtener datos históricos

def get_datos_historicos(tickers, start_date="2020-01-01"):
    """
    Obtiene los datos históricos de los tickers especificados.

    Parámetros:
    - Tickers: Lista con los tickers de los cuales se desea obtener los datos históricos.
    - start_date: Fecha de inicio de los datos históricos. Por defecto es "2020-01-01".

    Retorna:
    - Un DataFrame con los datos históricos de los tickers especificados.
    """
 
    end_date = datetime.now().strftime('%Y-%m-%d')
    datos_historicos_yf = yf.download(tickers, start=start_date, end=end_date, progress=False, group_by="ticker")

    if isinstance(datos_historicos_yf.columns, pd.MultiIndex):
        datos_historicos_yf.columns = ['_'.join(col).strip() for col in datos_historicos_yf.columns]
    datos_historicos_yf = datos_historicos_yf.copy()
    datos_historicos_yf.reset_index(inplace=True)
    datos_historicos_yf = datos_historicos_yf.melt(id_vars=['Date'], var_name="Variable", value_name="Valor")
    datos_historicos_yf[['Ticker', 'Metric']] = datos_historicos_yf['Variable'].str.rsplit('_', n=1, expand=True)
    datos_historicos_yf = datos_historicos_yf.pivot(index=['Date', 'Ticker'], columns='Metric', values='Valor').reset_index()
    print('Datos historicos descargados con exito')

    return datos_historicos_yf

