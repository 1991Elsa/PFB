import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
import time

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


# Función para obtener los datos financieros

def get_financials_yf(tickers):
    """
    Obtiene los estados financieros de los tickers especificados.

    Parámetros:
    - Tickers: Lista con los tickers de los cuales se desea obtener los estados financieros.

    Retorna:
    - Un DataFrame con los estados financieros de los tickers especificados.
    """
    datos_financieros_yf = {}
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        financials = stock.financials.T  # Transpuesta para tener las fechas como índices
        financials.reset_index(inplace=True)
        financials = financials.melt(id_vars=['index'], var_name="Fecha", value_name="Valor")
        financials['Ticker'] = ticker
        financials['Metric'] = financials['index']
        financials = financials.drop(columns=['index'])
        datos_financieros_yf[ticker] = financials
    
    datos_financieros_yf = pd.concat(datos_financieros_yf.values(), ignore_index=True)
    datos_financieros_yf = datos_financieros_yf.pivot(index=['Fecha', 'Ticker'], columns='Metric', values='Valor').reset_index()

    print('Datos financieros descargados con éxito')

    return datos_financieros_yf

# Función que obtiene los flujos de caja, reflejan el dinero que entra y sale de las empresas.
def get_cashflow_yf(tickers):
    """
    Obtiene los flujos de caja de los tickers especificados.

    Parámetros:
    - Tickers: Lista con los tickers de los cuales se desea obtener los flujos de caja.

    Retorna:
    - Un DataFrame con los flujos de caja de los tickers especificados.
    """
    datos_cashflow_yf = {}
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        cashflow = stock.cashflow.T  # Transpuesta para tener las fechas como índices
        cashflow.reset_index(inplace=True)
        cashflow = cashflow.melt(id_vars=['index'], var_name="Fecha", value_name="Valor")
        cashflow['Ticker'] = ticker
        cashflow['Metric'] = cashflow['index']
        cashflow = cashflow.drop(columns=['index'])
        datos_cashflow_yf[ticker] = cashflow
    
    datos_cashflow_yf = pd.concat(datos_cashflow_yf.values(), ignore_index=True)
    datos_cashflow_yf = datos_cashflow_yf.pivot(index=['Fecha', 'Ticker'], columns='Metric', values='Valor').reset_index()

    print('Datos de Cash Flow descargados con éxito')

    return datos_cashflow_yf


# Función para obtener los datos trimestrales de ganancias de las empresas.
# Función para obtener los resultados trimestrales de ganancias de las empresas
def get_earnings_yf(tickers):
    """
    Obtiene los resultados trimestrales de los tickers especificados.

    Parámetros:
    - Tickers: Lista con los tickers de los cuales se desea obtener los resultados trimestrales.

    Retorna:
    - Un DataFrame con los resultados trimestrales de los tickers especificados.
    """
    datos_earnings_yf = {}
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        
        try:
            earnings = stock.income_stmt.T 
            earnings.reset_index(inplace=True)
            earnings = earnings.melt(id_vars=['index'], var_name="Fecha", value_name="Valor")
            earnings['Ticker'] = ticker
            earnings['Metric'] = earnings['index']
            earnings = earnings.drop(columns=['index'])
            datos_earnings_yf[ticker] = earnings
        except Exception as e:
            print(f"Error al obtener datos de earnings para {ticker}: {e}")
            continue
    
    datos_earnings_yf = pd.concat(datos_earnings_yf.values(), ignore_index=True)
    datos_earnings_yf = datos_earnings_yf.pivot(index=['Fecha', 'Ticker'], columns='Metric', values='Valor').reset_index()

    print('Datos de Earnings descargados con éxito')

    return datos_earnings_yf



# Función que muestra los activos, pasivos y el patrimonio neto de las empresas en tal momento.

def get_balance_sheet_yf(tickers):
    """
    Obtiene los balances de los tickers especificados.

    Parámetros:
    - Tickers: Lista con los tickers de los cuales se desea obtener los balances.

    Retorna:
    - Un DataFrame con los balances de los tickers especificados.
    """
    datos_balance_sheet_yf = {}
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        balance_sheet = stock.balance_sheet.T  # Transpuesta para tener las fechas como índices
        balance_sheet.reset_index(inplace=True)
        balance_sheet = balance_sheet.melt(id_vars=['index'], var_name="Fecha", value_name="Valor")
        balance_sheet['Ticker'] = ticker
        balance_sheet['Metric'] = balance_sheet['index']
        balance_sheet = balance_sheet.drop(columns=['index'])
        datos_balance_sheet_yf[ticker] = balance_sheet
    
    datos_balance_sheet_yf = pd.concat(datos_balance_sheet_yf.values(), ignore_index=True)
    datos_balance_sheet_yf = datos_balance_sheet_yf.pivot(index=['Fecha', 'Ticker'], columns='Metric', values='Valor').reset_index()

    print('Datos de Balance Sheet descargados con éxito')

    return datos_balance_sheet_yf

# Función para obtener dividendos y splits de las acciones.

def get_actions_yf(tickers):
    """
    Obtiene los eventos de acciones (dividendos y splits) de los tickers especificados.
    
    Parámetros:
    - tickers: Lista con los tickers de los cuales se desea obtener los eventos de acciones (dividendos y splits).
    
    Retorna:
    - Un DataFrame con los eventos de acciones (dividendos y splits) de los tickers especificados.
    """
    eventos_acciones = {}
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        acciones = stock.actions  
        acciones.reset_index(inplace=True)
        acciones = acciones.melt(id_vars=['Date'], var_name="Acción", value_name="Valor")
        acciones['Ticker'] = ticker
        acciones['Tipo de Evento'] = acciones['Acción'].apply(lambda x: 'Dividendo' if x == 'dividend' else 'Split')
        acciones = acciones.drop(columns=['Acción'])
        eventos_acciones[ticker] = acciones

    eventos_acciones_yf = pd.concat(eventos_acciones.values(), ignore_index=True)
    eventos_acciones_yf = eventos_acciones_yf.pivot(index=['Date', 'Ticker'], columns='Tipo de Evento', values='Valor').reset_index()

    print('Eventos de acciones (dividendos y splits) descargados con éxito')

    return eventos_acciones_yf


# Ejecutar cada función y mostrar los primeros 3 registros de los df

tickers = tickers_nasdaq()

datos_historicos = get_datos_historicos(tickers)
print(datos_historicos.head(3))

datos_financieros = get_financials_yf(tickers)
print(datos_financieros.head(3))

datos_cashflow = get_cashflow_yf(tickers)
print(datos_cashflow.head(3))

datos_earnings = get_earnings_yf(tickers)
print(datos_earnings.head(3))

datos_balance_sheet = get_balance_sheet_yf(tickers)
print(datos_balance_sheet.head(3))


eventos_acciones = get_actions_yf(tickers)
print(eventos_acciones.head(3))

"""
solo pruebas de funciones/metodos de yfinance para obtener mas 
metricas historicas para posible analisis o tablero de power bi 
"""