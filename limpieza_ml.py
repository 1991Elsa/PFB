import pandas as pd
import numpy as np
from descarga_sql import descargar_data_sql

nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

# INCLUIR EN LA LIMPIEZA_DF para el manejo de Nans

# Limpieza de datos info

nasdaq_tickers_info ["DividendRate"].fillna(0, inplace=True)
nasdaq_tickers_info ["DividendYield"].fillna(0, inplace=True)

nasdaq_tickers_info["ReturnOnAssets"] = nasdaq_tickers_info.groupby("Sector")["ReturnOnAssets"].transform(lambda x: x.fillna(x.median()))
nasdaq_tickers_info["ReturnOnEquity"] = nasdaq_tickers_info.groupby("Sector")["ReturnOnEquity"].transform(lambda x: x.fillna(x.median()))
nasdaq_tickers_info["DebtToEquity"] = nasdaq_tickers_info.groupby("Sector")["DebtToEquity"].transform(lambda x: x.fillna(x.median()))
nasdaq_tickers_info["FreeCashflow"] = nasdaq_tickers_info.groupby("Sector")["FreeCashflow"].transform(lambda x: x.fillna(x.median()))


# Limpieza de datos historic



nans = nasdaq_tickers_historic[nasdaq_tickers_historic.isna().any(axis=1)]

def buscar_linealidad_temporal_nan(df):
    rango_fechas= pd.date_range(start= df["Date"].min(), end= df["Date"].max(), freq='MS')
    return rango_fechas.isin(df["Date"].dt.to_period("M").dt.to_timestamp()).all()

tickers_linealidad_temporal_nan = nans.groupby("Ticker").apply(buscar_linealidad_temporal_nan)

tickers_linealidad_temporal_nan = tickers_linealidad_temporal_nan[tickers_linealidad_temporal_nan].index.tolist()
print("Tickers de empresas con fechas continuas en las filas con valores nulos:", tickers_linealidad_temporal_nan)

nasdaq_tickers_historic = nasdaq_tickers_historic[~nasdaq_tickers_historic["Ticker"].isin(tickers_linealidad_temporal_nan)]

sin_linealidad_temporal = tickers_linealidad_temporal_nan[~tickers_linealidad_temporal_nan].index.tolist()
print("Tickers de empresas con fechas no continuas en las filas con valores nulos:", sin_linealidad_temporal)

nasdaq_tickers_historic = nasdaq_tickers_historic.sort_values(by=["Ticker", "Date"])

tickers_sin_linealidad_temporal = nans[nans["Ticker"].isin(sin_linealidad_temporal)]["Ticker"].unique()

nasdaq_tickers_historic.loc[tickers_sin_linealidad_temporal, ["Close", "High", "Low", "Open", "Volume"]] = (nasdaq_tickers_historic.loc[tickers_sin_linealidad_temporal].set_index("Date")[["Close", "High", "Low", "Open", "Volume"]].interpolate(method="time", limit_direction="both").values)

print("Valores nulos después de la interpolación:")
print(nasdaq_tickers_historic.isna().sum())

