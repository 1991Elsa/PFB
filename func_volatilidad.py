import pandas as pd
import numpy as np
from funcion_extraccion_info_historicos import nasdaq_tickers_historic


def calcular_volatilidad(ticker, df, periodo="diario"):
    """
    Calcula la volatilidad de los tickers del Nasdaq 100 usando la desviación estándar
    de los rendimientos diarios o mensuales.

    Parámetros:
    - ticker (str): Símbolo del ticker de la acción.
    - df (DataFrame): DataFrame con los datos históricos ('Date', 'Ticker', 'Close').
    - periodo: "diario" o "mensual"

    Retorna:
    - DataFrame con la volatilidad de cada ticker.
    """

    df_ticker = df[df['Ticker'] == ticker].sort_values(by='Date')

    # Calcular rendimientos
    if periodo == "diario":
        rendimientos = datos.pct_change()
    elif periodo == "mensual":
        rendimientos = datos.resample('M').last().pct_change()
    else:
        raise ValueError("El periodo debe ser 'diario' o 'mensual'.")

    # Calcular volatilidad (desviación estándar de los rendimientos)
    volatilidad = rendimientos.std()

    # Convertir a DataFrame ordenado
    df_volatilidad = pd.DataFrame({'Ticker': volatilidad.index, 'Volatilidad': volatilidad.values})
    df_volatilidad = df_volatilidad.sort_values(by="Volatilidad", ascending=False).reset_index(drop=True)

    return df_volatilidad

# Calcular volatilidad diaria
volatilidad_diaria = calcular_volatilidad(ticker, df, periodo="diario")
print(volatilidad_diaria)

# Calcular volatilidad mensual
volatilidad_mensual = calcular_volatilidad(ticker, df, periodo="mensual")
print(volatilidad_mensual)