import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np



def tickers_nasdaq():
    url = 'https://es.tradingview.com/symbols/NASDAQ-NDX/components/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    tickers = []
    for row in soup.find_all('tr', {'class': 'row-RdUXZpkv'}):
        data_row = row.get('data-rowkey', '')
        if data_row.startswith('NASDAQ:'):
            tickers.append(data_row.replace('NASDAQ:', ''))
    return tickers

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
for ticker in tickers:
    ticker_info = get_ticker_info(ticker)
    dic_info = {
        'Ticker': ticker_info.get('symbol', ticker),
        'ShortName': ticker_info.get('shortName', 'N/A'),
        'Sector': ticker_info.get('sector', 'N/A'),
        'Industry': ticker_info.get('industry', 'N/A'),
        'Country': ticker_info.get('country', 'N/A'),
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
        "ebitdaMargins": ticker_info.get('ebitdaMargins', 'N/A'),
    }
    df_info = pd.DataFrame([dic_info])

    # Añadir la información al DataFrame de todos los tickers
    nasdaq_tickers_info = pd.concat([nasdaq_tickers_info, df_info], ignore_index=True)

# Mostrar las primeras filas de los DataFrames resultantes

print(nasdaq_tickers_info.head())
print(nasdaq_tickers_historic.head().to_string(index=False))

# Convertir en csv para pasar a otro notebook
nasdaq_tickers_info.to_csv("nasdaq_info", index=False)
nasdaq_tickers_historic.to_csv("nasdaq_historic", index=False)
