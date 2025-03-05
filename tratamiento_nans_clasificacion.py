import pandas as pd
import numpy as np
from descarga_sql import nasdaq_tickers_historic


def tratamiento_nans_historic_rf(df):
    """
  
    """
    try:
        date_limit = df["Date"].max() - pd.DateOffset(years=2)
        df = df[df["Date"] >= date_limit].copy()

        nans = df[df.isna().any(axis=1)]

        def verificar_linealidad_temporal(df):
            df["Date"] = pd.to_datetime(df["Date"])
            fechas = pd.date_range(start=df["Date"].min(), end=df["Date"].max(), freq="MS")
            return fechas.isin(df["Date"]).all()
        
        tickers_con_linealidad = (nans.groupby("Ticker").apply(verificar_linealidad_temporal).loc[lambda x: x].index.tolist())

        sin_linealidad_temporal = list(set(nans["Ticker"]) - set(tickers_con_linealidad))

        # Eliminar las filas en las que  el ticker está en la lista de linealidad temporal
        df = df[~df["Ticker"].isin(tickers_con_linealidad)].reset_index(drop=True)

        # Interpolar datos para los tickers sin linealidad temporal
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values(["Ticker", "Date"])

        for ticker in sin_linealidad_temporal:
            ticker_sin_linealidad = df["Ticker"] == ticker
            df.loc[ticker_sin_linealidad, ["Close", "High", "Low", "Open", "Volume"]] = (
            df.loc[ticker_sin_linealidad].set_index("Date")[["Close", "High", "Low", "Open", "Volume"]]
            .interpolate(method="time", limit_direction="both").values)

        df = df.reset_index(drop=True)

        col_to_float32 = ["Close", "High", "Low", "Open", "Volume", "Cluster"]
        nasdaq_tickers_historic[col_to_float32] = nasdaq_tickers_historic[col_to_float32].astype("float32")

        print("Valores nulos después de tratamiento:")
        print(df.isna().sum())
        print("Información del dataframe después del tratamiento:")
        print(nasdaq_tickers_historic.info())

    except Exception as e:
        print(f'Fallo el tratamiento de nans historic cluster {e}')
    return nasdaq_tickers_historic

nasdaq_tickers_historic = tratamiento_nans_historic_rf(nasdaq_tickers_historic)

