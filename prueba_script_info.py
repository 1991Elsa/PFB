import yfinance as yf
import pandas as pd
from datetime import datetime
import time
from tickers_nasdaq import tickers_nasdaq

def get_datos_historicos (ticker, start_date="2020-01-01"):
    #funcion para sacar datos historicos de un ticker

    end_date = datetime.now().strftime('%Y-%m-%d')

    datos = yf.download(ticker, start = start_date, end = end_date)

    return datos

def get_ticker_info (ticker):
    #funcion para sacar información de un ticker individual
    ticker_info = yf.Ticker(ticker).info

    return ticker_info

nasdaq_tickers_info = pd.DataFrame() 

for ticker in tickers_nasdaq:
    #llamamos a las funciones para extraer data del ticker
    ticker_info = get_ticker_info(ticker)

    ticker_historic = get_datos_historicos(ticker)
    
    #cogemos la info individual que nos interesa
    dic_info= {'Ticker': ticker_info['symbol'],'sector': ticker_info['sector'], 'industry': ticker_info['industry'],'shares' : ticker_info['sharesOutstanding'] }
    
    df = pd.DataFrame([dic_info])

    #cambiamos de orientacion el df de datos historicos
    dft = ticker_historic.T.reset_index()

    #hacemos merge de los dos df
    dfmerge= pd.merge(df, dft, on='Ticker') 

    #guardamos en un df final concatenando toda la info
    nasdaq_tickers_info = pd.concat([nasdaq_tickers_info, dfmerge], ignore_index=True)


