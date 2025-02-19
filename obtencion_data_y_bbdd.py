import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
import time
from tablas_metadata import *
from connect_engine import *



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

    return nasdaq_tickers_info

# Función para limpiar los datos
def clean_data(df):
    df = df.round(2)
    df = df.replace({np.nan:None})

    return df

# Creacion de la tabla en MySQL
def creacion_bbdd(df_info_clean, df_historic_clean):
    try:
        initial_engine = get_engine()
        with initial_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión inicial establecida con éxito y librerías instaladas correctamente.")
        
        # Conectarse y crear la base de datos 'yahoo_finance' si no existe
        with initial_engine.connect() as connection:
            connection.execute(text("CREATE DATABASE IF NOT EXISTS yahoo_finance"))
            print("Base de datos yahoo_finance creada con éxito.")
        
        # Ahora conectar al motor especificando la nueva base de datos
        engine = get_engine_database()
        # Verificar la conexión a la nueva base de datos
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión establecida con éxito a la base de datos yahoo_finance y librerías instaladas correctamente.")
    except Exception as e:
        print(f"Error al establecer la conexión: {e}")

    # Crear las tablas en la base de datos
    try:
        metadata.create_all(engine, checkfirst=True)
        print("Tablas creadas con éxito.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

    # subir los df
    try:

        df_nasdaq_tickers_info_clean = pd.read_csv('nasdaq_tickers_info_clean.csv')
        df_nasdaq_tickers_historic_clean = pd.read_csv('nasdaq_tickers_historic_clean.csv')

        # Asegurarse de que las columnas 'Timestamp_extraction' y 'Date' son del tipo correcto
        df_nasdaq_tickers_info_clean['Timestamp_extraction'] = pd.to_datetime(df_nasdaq_tickers_info_clean['Timestamp_extraction'])
        df_nasdaq_tickers_historic_clean['Date'] = pd.to_datetime(df_nasdaq_tickers_historic_clean['Date']).dt.date

        # Reemplazar NaN por None
        df_nasdaq_tickers_info_clean = df_nasdaq_tickers_info_clean.replace({np.nan: None})
        df_nasdaq_tickers_historic_clean = df_nasdaq_tickers_historic_clean.replace({np.nan: None})

        # Desactivar las restricciones de clave foránea temporalmente
        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))

        # Insertar los datos en la tabla nasdaq_tickers_info_sql sin cambiar su estructura
        try:
            with engine.begin() as conn:
                for row in df_nasdaq_tickers_info_clean.to_dict(orient='records'):
                    stmt = insert(tickers_info_table).values(**row)
                    conn.execute(stmt)
            print("Datos insertados en la tabla nasdaq_tickers_info_sql correctamente.")
        except Exception as e:
            print(f"Error al insertar los datos en la tabla nasdaq_tickers_info_sql: {e}")

        # Insertar los datos en la tabla nasdaq_tickers_historic_sql sin cambiar su estructura
        try:
            with engine.begin() as conn:
                for row in df_nasdaq_tickers_historic_clean.to_dict(orient='records'):
                    stmt = insert(tickers_historic_table).values(**row)
                    conn.execute(stmt)
            print("Datos insertados en la tabla nasdaq_tickers_historic_sql correctamente.")
        except Exception as e:
            print(f"Error al insertar los datos en la tabla nasdaq_tickers_historic_sql: {e}")

        # Reactivar las restricciones de clave foránea
        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

    except Exception as e:
        print(f"Error al leer los archivos CSV o insertar los datos en las tablas: {e}")



#Bucle para automatizar la extracción de datos

while True:
    now=datetime.now().strftime('%H:%M')
    market_close = '16:00'
    if now == market_close:
        #if True:
    # Obtener la lista de tickers del NASDAQ

        tickers = tickers_nasdaq()

        # Obtener los datos históricos de todos los tickers del NASDAQ

        nasdaq_tickers_historic = get_datos_historicos(tickers)
        nasdaq_tickers_historic_clean = clean_data(nasdaq_tickers_historic)


        # Obtener la información de los tickers

        nasdaq_tickers_info = obtener_informacion_tickers(tickers)
        nasdaq_tickers_info_clean = clean_data(nasdaq_tickers_info)

        #Guardar los DataFrames como archivos CSV
        nasdaq_tickers_info_clean.to_csv('nasdaq_tickers_info_clean.csv', index=False)
        nasdaq_tickers_historic_clean.to_csv('nasdaq_tickers_historic_clean.csv', index=False)

        # Crear la base de datos y las tablas
        creacion_bbdd(nasdaq_tickers_info_clean, nasdaq_tickers_historic_clean)


        break
    
    else:
        time.sleep(3600)