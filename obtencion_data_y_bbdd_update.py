import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
import time
from connect_engine import *
from tablas_metadata import *
from sqlalchemy.dialects.mysql import insert

# Función para obtener los tickers de NASDAQ 100 (scrapping)
def tickers_nasdaq():
    """
Extrae mediante scrapping en la pagina TradingView los tickers de NASDAQ 100 actualizados.

Parámetros:
- No tiene.

Retorna:
- Una lista con los tickers de NASDAQ 100.
"""

    
     
    url = 'https://es.tradingview.com/symbols/NASDAQ-NDX/components/'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')


    tickers = []
    tickers.append('NDX')
    for row in soup.find_all('tr', {'class': 'row-RdUXZpkv'}):
        data_row = row.get('data-rowkey', '')
        if data_row.startswith('NASDAQ:'):
            tickers.append(data_row.replace('NASDAQ:', ''))
    print('Tickers scrapeados con exito')
    return tickers


# Función para obtener datos históricos

def get_datos_historicos(tickers, start_date="2020-01-01"):
    """
Obtiene los datos históricos de los tickers especificados.

Parámetros:
- Tickers: Lista con los tickers de los cuales se desea obtener los datos históricos.
- start_date: Fecha de inicio de los datos históricos. Por defecto es "2020-01-01".

Retorna:
- Un DataFrame con los datos históricos de los tickers especificados.
"""
 
    end_date = datetime.now().strftime('%Y-%m-%d')
    datos = yf.download(tickers, start=start_date, end=end_date, progress=False, group_by="ticker")

    if isinstance(datos.columns, pd.MultiIndex):
        datos.columns = ['_'.join(col).strip() for col in datos.columns]
    datos = datos.copy()
    datos.reset_index(inplace=True)
    datos = datos.melt(id_vars=['Date'], var_name="Variable", value_name="Valor")
    datos[['Ticker', 'Metric']] = datos['Variable'].str.rsplit('_', n=1, expand=True)
    datos = datos.pivot(index=['Date', 'Ticker'], columns='Metric', values='Valor').reset_index()
    print('Datos historicos descargados con exito')

    return datos
    

# Función para obtener información de un ticker

def get_ticker_info(ticker):
    """
Obtiene la información de un ticker.

Parámetros:
- Tickers: Ticker del cual se desea obtener la información.

Retorna:
- Un diccionario con la información del ticker especificado.
"""

    ticker_info = yf.Ticker(ticker).info

    return ticker_info

# Función para obtener la información de los tickers

def obtener_informacion_tickers(tickers):
    """
Obtiene la información especifica y util de los tickers especificados.

Parámetros:
- Tickers: Lista con los tickers de los cuales se desea obtener los datos históricos.

Retorna:
- Un DataFrame con la información de los tickers especificados.
"""

    nasdaq_tickers_info = pd.DataFrame()

    for ticker in tickers:

        if ticker != 'NDX':
            ticker_info = get_ticker_info(ticker)
            dic_info = {
                'Ticker': ticker_info.get('symbol', ticker), 
                'ShortName': ticker_info.get('shortName', 'N/A'), 
                'Sector': ticker_info.get('sector', 'N/A'),
                'Industry': ticker_info.get('industry', 'N/A'),
                'Country': ticker_info.get('country', 'N/A'),
                'MarketCap': ticker_info.get('marketCap', 'N/A'), 
                'TotalRevenue': ticker_info.get('totalRevenue', 'N/A'), 
                'NetIncomeToCommon': ticker_info.get('netIncomeToCommon', 'N/A'),
                'ReturnOnAssets': ticker_info.get('returnOnAssets', 'N/A'), 
                'ReturnOnEquity': ticker_info.get('returnOnEquity', 'N/A'), 
                'DebtToEquity': ticker_info.get('debtToEquity', 'N/A'), 
                'FreeCashflow': ticker_info.get('freeCashflow', 'N/A'), 
                'DividendRate': ticker_info.get('dividendRate', 'N/A'), 
                'DividendYield': ticker_info.get('dividendYield', 'N/A'),
                'PayoutRatio': ticker_info.get('payoutRatio', 'N/A'),
                'GrossMargins': ticker_info.get('grossMargins', 'N/A'), 
                'OperatingMargins': ticker_info.get('operatingMargins', 'N/A'), 
                'ProfitMargins': ticker_info.get('profitMargins', 'N/A'),
                'ebitdaMargins': ticker_info.get('ebitdaMargins', 'N/A'), 
                'Timestamp_extraction': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            df_info = pd.DataFrame([dic_info])

            nasdaq_tickers_info = pd.concat([nasdaq_tickers_info, df_info], ignore_index=True)
            
    print('Informacion de los tickers descargada con exito')
    return nasdaq_tickers_info

# Función para limpiar los datos
def clean_data_info(df):
    """
    Limpia el dataframe de información de los tickers, para convertir las columnas numéricas en millones.
    Trata los valores nulos de las columnas numéricas, rellenando con la mediana de la columna agrupada por Sector o con 0 en caso de DividendRate y DividendYield.

    Parámetro: Dataframe con información de los tickers.

    Retorna: Dataframe limpio.
    """
    try:
        columnas_a_procesar = [
            'ReturnOnAssets', 'ReturnOnEquity', 'DebtToEquity', 'MarketCap',
            'TotalRevenue', 'NetIncomeToCommon', 'FreeCashflow', 'DividendRate',
            'DividendYield', 'PayoutRatio', 'ebitdaMargins'
        ]

        for columna in columnas_a_procesar:
            if columna in df.columns:  # Verificar si la columna existe en el dataframe
                df[columna] = pd.to_numeric(df[columna], errors='coerce')
                if columna in ['MarketCap', 'TotalRevenue', 'NetIncomeToCommon', 'FreeCashflow']:
                    df[columna] = df[columna] / 1_000_000  

        #Tratamiento de nans    
        df = df.fillna({"DividendRate" : 0, "DividendYield" : 0})

        df[columnas_a_procesar] = df.groupby("Sector")[columnas_a_procesar].transform(lambda x: x.fillna(x.median()))

        print("Valores nulos después del tratamiento:")
        print(df.isna().sum())
    
    except Exception as e:
        print(f'Fallo la limpieza de info {e}')
    
    return df


# Función para limpiar los datos historicos
def clean_data_historic(df):
    """
    Limpia el dataframe con la información historica de los tickers, para convertir las columnas a valores numéricos.
    Trata los valores nulos identificando la linealidad temporal de los datos y eliminando los tickers que cumplen con esta característica; porque son 
    empresas que aún no habían entrado al mercado en el rango de fechas de la descarga. Para los tickers restantes, interpola los valores nulos.

    Parámetro: Dataframe con información historica de los tickers.

    Retorna: Dataframe limpio.
    """
    
    try:
        columnas_a_procesar = [
            'Close', 'High', 'Low', 'Open', 'Volume'
        ]

        for columna in columnas_a_procesar:
            if columna in df.columns:  # Verificar si la columna existe en el dataframe
                df[columna] = pd.to_numeric(df[columna], errors='coerce')

        #Tratamiento de nans
        nans = df[df.isna().any(axis=1)]

        def verificar_linealidad_temporal(df):
            df["Date"] = pd.to_datetime(df["Date"])
            fechas = pd.date_range(start=df["Date"].min(), end=df["Date"].max(), freq="MS")
            return fechas.isin(df["Date"]).all()
        
        tickers_con_linealidad = (nans.groupby("Ticker").apply(verificar_linealidad_temporal).loc[lambda x: x].index.tolist())

        sin_linealidad_temporal = list(set(nans["Ticker"]) - set(tickers_con_linealidad))

        # Eliminar las filas en las que  el ticker está en la lista de linealidad temporal
        df = df[~df["Ticker"].isin(tickers_con_linealidad)].reset_index(drop=True)

        df = df.reset_index(drop=True)

        print("Valores nulos después de tratamiento:")
        print(df.isna().sum())

    except Exception as e:
        print(f'Fallo la limpieza de historic {e}')
    return df


# Creacion de la BBDD en MySQL
def creacion_bbdd(df_info_clean, df_historic_clean):
    
    try:
        initial_engine = get_engine()
        with initial_engine.connect() as connection:
            result = connection.execute(text("CREATE DATABASE IF NOT EXISTS yahoo_finance"))
            print("Base de datos 'yahoo_finance' creada/verificada con éxito.")
        
        # Conectarse a la base de datos 'yahoo_finance'
        engine = get_engine_database()
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión establecida con éxito a la base de datos yahoo_finance.")
    except Exception as e:
        print(f"Error al establecer la conexión: {e}")

    # Crea las tablas en la base de datos
    try:
        metadata.create_all(engine, checkfirst=True)
        print("Tablas creadas/verificadas con éxito.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

    # Subir los df
    try:
        df_nasdaq_tickers_info_clean = pd.read_csv('nasdaq_tickers_info_clean.csv')
        df_nasdaq_tickers_historic_clean = pd.read_csv('nasdaq_tickers_historic_clean.csv')

        # Asegura el type de las columnas 'Timestamp_extraction' y 'Date' 
        df_nasdaq_tickers_info_clean['Timestamp_extraction'] = pd.to_datetime(df_nasdaq_tickers_info_clean['Timestamp_extraction'])
        df_nasdaq_tickers_historic_clean['Date'] = pd.to_datetime(df_nasdaq_tickers_historic_clean['Date']).dt.date

        # Reemplazar NaN por None para que no falle sql
        df_nasdaq_tickers_info_clean = df_nasdaq_tickers_info_clean.replace({np.nan: None})
        df_nasdaq_tickers_historic_clean = df_nasdaq_tickers_historic_clean.replace({np.nan: None})

        # Desactivar las restricciones de clave foránea temporalmente para el llenado
        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))

        # Insertar/actualizar los datos en nasdaq_tickers_info_sql
        try:
            with engine.begin() as conn:
                data = df_info_clean.to_dict(orient='records')
                stmt = insert(tickers_info_table).values(data)
                update_dict = {c.name: c for c in stmt.inserted if c.name != 'Ticker'}
                stmt = stmt.on_duplicate_key_update(update_dict)
                conn.execute(stmt)
            print("Datos insertados en nasdaq_tickers_info_sql correctamente.")
        except Exception as e:
            print(f"Error al insertar datos en nasdaq_tickers_info_sql: {e}")

        # Insertar/actualizar los datos en nasdaq_tickers_historic_sql
        try:
            with engine.begin() as conn:
                data = df_historic_clean.to_dict(orient='records')
                stmt = insert(tickers_historic_table).values(data)
                update_dict = {c.name: c for c in stmt.inserted if c.name not in ['Date', 'Ticker']}
                stmt = stmt.on_duplicate_key_update(update_dict)
                conn.execute(stmt)
            print("Datos insertados en nasdaq_tickers_historic_sql correctamente.")
        except Exception as e:
            print(f"Error al insertar datos en nasdaq_tickers_historic_sql: {e}")

        # Reactiva la clave foránea
        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

    except Exception as e:
        print(f"Error al procesar los datos: {e}")

# Ejecución de las funciones
try:
    tickers = tickers_nasdaq()
except Exception as e:
    print(f'Error en la función de scrapping: {e}')
    
# Obtener y limpiar datos históricos
try:
    datos_historicos = get_datos_historicos(tickers)
    nasdaq_tickers_historic_clean = clean_data_historic(datos_historicos)
except Exception as e:
    print(f'Error en la llamada de históricos: {e}')

# Obtener y limpiar información de los tickers
try:
    informacion_tickers = obtener_informacion_tickers(tickers)
    nasdaq_tickers_info_clean = clean_data_info(informacion_tickers)
except Exception as e:
    print(f'Error en la llamada de info: {e}')

# Guardar los DataFrames como archivos CSV
try:
    nasdaq_tickers_info_clean.to_csv('nasdaq_tickers_info_clean.csv', index=False)
    nasdaq_tickers_historic_clean.to_csv('nasdaq_tickers_historic_clean.csv', index=False)
except Exception as e:
    print(f'Error en la limpieza de los datos: {e}')

# Crear la bbdd y las tablas
try:
    creacion_bbdd(nasdaq_tickers_info_clean, nasdaq_tickers_historic_clean)
except Exception as e:
    print(f'No se creó la BBDD: {e}')
