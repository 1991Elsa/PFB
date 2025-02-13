import yfinance as yf
import pandas as pd
from datetime import datetime
import time
from tickers_nasdaq import tickers_nasdaq

def get_datos_historicos (ticker, start_date="2020-01-01"):

    end_date = datetime.now().strftime('%Y-%m-%d')

    datos = yf.download(ticker, start = start_date, end = end_date)

    return datos

def get_ticker_info (ticker):
    ticker_info = yf.Ticker(ticker).info
    return ticker_info

nasdaq_tickers_info = pd.DataFrame()

for ticker in tickers_nasdaq:
    ticker_info = get_ticker_info(ticker)
    ticker_historic = get_datos_historicos(ticker)
    dic_info= {'Ticker': ticker_info['symbol'],'sector': ticker_info['sector'], 'industry': ticker_info['industry'],'shares' : ticker_info['sharesOutstanding'] }
    df = pd.DataFrame([dic_info])
    dft = ticker_historic.T.reset_index()
    dfmerge= pd.merge(df, dft, on='Ticker') 
    nasdaq_tickers_info = pd.concat([nasdaq_tickers_info, dfmerge], ignore_index=True)


