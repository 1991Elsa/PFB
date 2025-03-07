import pandas as pd
import numpy as np
from descarga_sql import nasdaq_tickers_historic

#print("Valores nulos antes de tratamiento:")
#print(nasdaq_tickers_historic.isna().sum())
#print("Información del dataframe antes del tratamiento:")
#print(nasdaq_tickers_historic.info())

def tratamiento_nans_historic_rf(df):
    """
    Trata los valores nulos de la tabla nasdaq_tickers_historic previo a ejecutar el modelo de clasificación. 
    Filtra los datos de los últimos dos años en los que se tienen resultados de clustering.
    Identifica la linealidad temporal de los datos y elimina los tickers que cumplen con esta característica; porque son 
    empresas que aún no habían entrado al mercado en el rango de fechas de la descarga. Para los tickers restantes, interpola los valores nulos.
    Elimina las columnas "Date" y "Ticker" porque no son relevantes para el modelo de clasificación.
    Cambia el tipo de datos de float64 a float32 para reducir el uso de memoria.

    Parámetro: Dataframe con información historica de los tickers y resultados del modelo de clustering.

    Retorna: Dataframe limpio y listo para usar en el modelo de clasificación.
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
        df[col_to_float32] = df[col_to_float32].astype("float32")
        df.drop(columns=["Date", "Ticker"], axis=1,  inplace=True)

        print("Valores nulos después del tratamiento:")
        print(df.isna().sum())
        print("Información del dataframe después del tratamiento:")
        print(df.info())

    except Exception as e:
        print(f'Fallo el tratamiento de nans historic cluster {e}')
    return df

nasdaq_tickers_historic = tratamiento_nans_historic_rf(nasdaq_tickers_historic)

