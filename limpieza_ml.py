import pandas as pd
import numpy as np
from descarga_sql import descargar_data_sql

nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

# Limpieza de datos info
nasdaq_tickers_info = nasdaq_tickers_info.fillna({"DividendRate" :0, "DividendYield" : 0})

columnas = ["ReturnOnAssets", "ReturnOnEquity", "DebtToEquity", "FreeCashflow" ]
nasdaq_tickers_info[columnas] = nasdaq_tickers_info.groupby("Sector")[columnas].transform(lambda x: x.fillna(x.median()))


# Limpieza de datos historic

nans = nasdaq_tickers_historic[nasdaq_tickers_historic.isna().any(axis=1)]

def verificar_linealidad_temporal(df):
    df["Date"] = pd.to_datetime(df["Date"])
    fechas = pd.date_range(start=df["Date"].min(), end=df["Date"].max(), freq="MS")
    return fechas.isin(df["Date"]).all()

tickers_con_linealidad = (nans.groupby("Ticker").apply(verificar_linealidad_temporal).loc[lambda x: x].index.tolist())

sin_linealidad_temporal = list(set(nans["Ticker"]) - set(tickers_con_linealidad))

# Eliminar los tickers con linealidad temporal
nasdaq_tickers_historic = nasdaq_tickers_historic[~nasdaq_tickers_historic["Ticker"].isin(tickers_con_linealidad)].reset_index(drop=True)

# Interpolar datos para los tickers sin linealidad temporal
nasdaq_tickers_historic["Date"] = pd.to_datetime(nasdaq_tickers_historic["Date"])
nasdaq_tickers_historic = nasdaq_tickers_historic.sort_values(["Ticker", "Date"])

for ticker in sin_linealidad_temporal:
    ticker_sin_linealidad = nasdaq_tickers_historic["Ticker"] == ticker
    nasdaq_tickers_historic.loc[ticker_sin_linealidad, ["Close", "High", "Low", "Open", "Volume"]] = (
    nasdaq_tickers_historic.loc[ticker_sin_linealidad].set_index("Date")[["Close", "High", "Low", "Open", "Volume"]]
    .interpolate(method="time", limit_direction="both").values)

nasdaq_tickers_historic = nasdaq_tickers_historic.reset_index(drop=True)

print("Valores nulos después de eliminación e interpolación:")
print(nasdaq_tickers_historic.isna().sum())

print(nasdaq_tickers_historic.isna().sum())
print(nasdaq_tickers_info.isna().sum())