import pandas as pd
import numpy as np

def clean_data_historic(df):

    columnas_a_procesar = [
        'Close', 'High', 'Low', 'Open', 'Volume'
    ]

    for columna in columnas_a_procesar:
        if columna in df.columns:  # Verificar si la columna existe en el dataframe
            df[columna] = pd.to_numeric(df[columna], errors='coerce')

    df = df.replace({np.nan: None})

    return df

#df_nasdaq_tickers_historic_clean = clean_data_historic(nasdaq_tickers_historic)


def clean_data_info(df):
    """
    Limpia el DataFrame que contiene la información general de los tickers.
    """
    df = df.replace({np.nan: None})
    return df

#df_nasdaq_tickers_info_clean = clean_data_info(nasdaq_tickers_info)


def clean_data_finanzas(df):

    columnas_a_procesar = [
        'ReturnOnAssets', 'ReturnOnEquity', 'DebtToEquity', 'MarketCap',
        'TotalRevenue', 'NetIncomeToCommon', 'FreeCashflow', 'DividendRate',
        'DividendYield', 'PayoutRatio', 'Beta', 'ebitdaMargins'
    ]

    for columna in columnas_a_procesar:
        if columna in df.columns:  # Verificar si la columna existe en el dataframe
            df[columna] = pd.to_numeric(df[columna], errors='coerce')
            if columna in ['MarketCap', 'TotalRevenue', 'NetIncomeToCommon', 'FreeCashflow']:
                df[columna] = df[columna] / 1_000_000  

    df = df.replace({np.nan: None})

    return df

#df_nasdaq_tickers_finanzas_clean = clean_data_finanzas(nasdaq_tickers_finanzas)


