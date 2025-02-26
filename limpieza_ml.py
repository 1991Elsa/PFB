import pandas as pd
import numpy as np
from descarga_sql import descargar_data_sql

nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

# INCLUIR EN LA LIMPIEZA_DF para el manejo de Nans

nasdaq_tickers_info ["DividendRate"].fillna(0, inplace=True)
nasdaq_tickers_info ["DividendYield"].fillna(0, inplace=True)

nasdaq_tickers_info["ReturnOnAssets"] = nasdaq_tickers_info.groupby("Sector")["ReturnOnAssets"].transform(lambda x: x.fillna(x.median()))
nasdaq_tickers_info["ReturnOnEquity"] = nasdaq_tickers_info.groupby("Sector")["ReturnOnEquity"].transform(lambda x: x.fillna(x.median()))
nasdaq_tickers_info["DebtToEquity"] = nasdaq_tickers_info.groupby("Sector")["DebtToEquity"].transform(lambda x: x.fillna(x.median()))
nasdaq_tickers_info["FreeCashflow"] = nasdaq_tickers_info.groupby("Sector")["FreeCashflow"].transform(lambda x: x.fillna(x.median()))


