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
def get_ticker_info(tickers):  
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
                'MarketCap': ticker_info.get('marketCap', 'N/A'), # capitalización de mercado
                'TotalRevenue': ticker_info.get('totalRevenue', 'N/A'), # ingresos totales
                'NetIncomeToCommon': ticker_info.get('netIncomeToCommon', 'N/A'), # ingresos netos
                'TrailingEPS': ticker_info.get('trailingEps', 'N/A'), # EPS (ganancias por acción)
                'ForwardEPS': ticker_info.get('forwardEps', 'N/A'), # EPS futuro
                'TrailingPE': ticker_info.get('trailingPE', 'N/A'), # PER (Price-to-Earnings Ratio)
                'ForwardPE': ticker_info.get('forwardPE', 'N/A'), # PER futuro
                'ReturnOnAssets': ticker_info.get('returnOnAssets', 'N/A'), # esto es el retorno sobre los activos ROA (Return on Assets)
                'ReturnOnEquity': ticker_info.get('returnOnEquity', 'N/A'), # esto es el retorno sobre el patrimonio ROA (Return on Equity)
                'DebtToEquity': ticker_info.get('debtToEquity', 'N/A'), # esto es la deuda sobre el patrimonio
                'FreeCashflow': ticker_info.get('freeCashflow', 'N/A'), # esto es el flujo de caja libre
                'DividendRate': ticker_info.get('dividendRate', 'N/A'), # esto es la tasa de dividendos
                'DividendYield': ticker_info.get('dividendYield', 'N/A'), # esto es el rendimiento de los dividendos
                'PayoutRatio': ticker_info.get('payoutRatio', 'N/A'), # Ratio de pago
                'Beta': ticker_info.get('beta', 'N/A'), # esto es una medida de la volatilidad de un activo en comparación con el mercado en general
                'GrossMargins': ticker_info.get('grossMargins', 'N/A'), # márgenes brutos
                'OperatingMargins': ticker_info.get('operatingMargins', 'N/A'), # márgenes operativos
                'ProfitMargins': ticker_info.get('profitMargins', 'N/A'),# márgenes de beneficio,
                'ebitdaMargins': ticker_info.get('ebitdaMargins', 'N/A'), # márgenes de ebitda
                'Timestamp_extraction': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            df_info = pd.DataFrame([dic_info])

            # Añadir la información al DataFrame de todos los tickers
            nasdaq_tickers_info = pd.concat([nasdaq_tickers_info, df_info], ignore_index=True)
    return nasdaq_tickers_info

df_nasdaq_tickers_info_clean = clean_data(nasdaq_tickers_info)
df_nasdaq_tickers_historic_clean = clean_data(nasdaq_tickers_historic)

