import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
import time
from connect_engine import *
from tablas_metadata_5 import *
from sqlalchemy.dialects.mysql import insert
from descarga_sql import descargar_data_sql
#from clustering_dbscan import clustering_process

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
- Tickers: Lista con los tickers de los cuales se desea obtener los datos.

Retorna:
- Un DataFrame con la información de los tickers especificados.
"""

    nasdaq_tickers_info = pd.DataFrame()

    for ticker in tickers:

        if ticker != 'NDX':
            ticker_info = get_ticker_info(ticker)
            dic_info = {
                'Ticker': ticker_info.get('symbol', ticker), 
                'ShortName': ticker_info.get('shortName', 'N/A'),      #Nombre empresa
                'Sector': ticker_info.get('sector', 'N/A'),            #Sector de la empresa
                'Industry': ticker_info.get('industry', 'N/A'),        #Industria a la que pertenece
                'Country': ticker_info.get('country', 'N/A'),          #País de origen
            }
            df_info = pd.DataFrame([dic_info])

            nasdaq_tickers_info = pd.concat([nasdaq_tickers_info, df_info], ignore_index=True)
            
    print('Informacion de los tickers descargada con exito')
    return nasdaq_tickers_info


# Función para obtener distintas métricas financieras segmentadas en 3 df

def obtener_informacion_finanzas_tickers(tickers):
    """
    Obtiene la información financiera de los tickers especificados, segmentando en 3 df,
    y aseguramos Timestamp en cada uno de ellos por si se usa cada df independientemente.

    Parámetros:
    - tickers: Lista con los tickers de los cuales se desea obtener la información financiera.

    Retorna:
    - Tres DataFrames: finanzas_operativas, finanzas_balanza, finanzas_dividendos
    """
    finanzas_operativas = pd.DataFrame()
    finanzas_balanza = pd.DataFrame()
    finanzas_dividendos = pd.DataFrame()

    for ticker in tickers:
        if ticker != 'NDX': 
            ticker_info = get_ticker_info(ticker)  

            # Méticas financieras operativas
            dic_operativas = {
                'Ticker': ticker_info.get('symbol', ticker),
                'ReturnOnAssets': ticker_info.get('returnOnAssets', 'N/A'),     #Retorno sobre activos son las ganancias netas divididas por los activos totales
                'ReturnOnEquity': ticker_info.get('returnOnEquity', 'N/A'),     #Retorno sobre patrimonio son las ganancias netas divididas por el patrimonio neto
                'OperatingMargins': ticker_info.get('operatingMargins', 'N/A'), #Margen operativo que es el beneficio operativo dividido por los ingresos
                'GrossMargins': ticker_info.get('grossMargins', 'N/A'),         #Margen bruto son los ingresos menos el costo de los bienes vendidos dividido por los ingresos
                'ProfitMargins': ticker_info.get('profitMargins', 'N/A'),       #Margen de beneficio que es el beneficio neto dividido por los ingresos
                'ebitdaMargins': ticker_info.get('ebitdaMargins', 'N/A')        #Margen EBITDA que es el beneficio antes de intereses, impuestos, depreciación y amortización
            }
            df_operativas = pd.DataFrame([dic_operativas])
            finanzas_operativas = pd.concat([finanzas_operativas, df_operativas], ignore_index=True)

            # Métricas financieras de balanza
            dic_balanza = {
                'Ticker': ticker_info.get('symbol', ticker),
                'MarketCap': ticker_info.get('marketCap', 'N/A'),                   #Capitalización de mercado es el precio de las acciones multiplicado por el número de acciones en circulación
                'TotalRevenue': ticker_info.get('totalRevenue', 'N/A'),             #Ingresos totales de la empresa en un periodo determinado
                'NetIncomeToCommon': ticker_info.get('netIncomeToCommon', 'N/A'),   #Beneficio neto atribuible a los accionistas comunes de la empresa
                'DebtToEquity': ticker_info.get('debtToEquity', 'N/A'),             #Deuda sobre patrimonio es la deuda total dividida por el patrimonio neto
                'FreeCashflow': ticker_info.get('freeCashflow', 'N/A')              #Flujo de caja libre es el efectivo generado por la empresa después de los gastos de capital
            }
            df_balanza = pd.DataFrame([dic_balanza])
            finanzas_balanza = pd.concat([finanzas_balanza, df_balanza], ignore_index=True)

            # Metrícas financieras de dividendos
            dic_dividendos = {
                'Ticker': ticker_info.get('symbol', ticker),
                'DividendRate': ticker_info.get('dividendRate', 'N/A'),     #Tasa de dividendos es la cantidad de dinero pagada por acción
                'DividendYield': ticker_info.get('dividendYield', 'N/A'),   #Rendimiento de dividendos es la tasa de dividendos dividida por el precio de las acciones
                'PayoutRatio': ticker_info.get('payoutRatio', 'N/A')        #Ratio de pago es la cantidad de dinero pagada en dividendos dividida por las ganancias netos
            }
            df_dividendos = pd.DataFrame([dic_dividendos])
            finanzas_dividendos = pd.concat([finanzas_dividendos, df_dividendos], ignore_index=True)

    print('Información financiera segmentada descargada con éxito')
    return finanzas_operativas, finanzas_balanza, finanzas_dividendos

# Función para obtener el timestamp

def obtener_timestamp_actual():
    """Obtenemos un df con timestamp actual para llenar la tabla time_stamp_sql."""
    return pd.DataFrame({
        'Timestamp_extraction': [datetime.now()]
    })

# Función para limpiar los datos historicos
def clean_data_historic(df):

    try:
         
        columnas_a_procesar = [
            'Close', 'High', 'Low', 'Open', 'Volume'
        ]

        for columna in columnas_a_procesar:
            if columna in df.columns:  # Verificar si la columna existe en el dataframe
                df[columna] = pd.to_numeric(df[columna], errors='coerce')

        
        df = df.replace({np.nan: None})

        return df
    except Exception as e:
        print(f'Fallo la limpieza de historicos {e}')


# Función para limpiar los datos info general
def clean_data_info(df):
    try:
        # Este df contiene la información general de cada empresa, solo necesitamos manejar valores nulos.
        df = df.replace({np.nan: None})
        return df
    except Exception as e:
        print(f'Fallo la limpieza de info general {e}')


# Función para limpiar los datos financieros operativos 
def clean_data_finanzas_operativas(df):
    try:
        columnas_a_procesar = [
            'ReturnOnAssets', 'ReturnOnEquity', 'OperatingMargins', 'GrossMargins',
            'ProfitMargins', 'ebitdaMargins'
        ]

        for columna in columnas_a_procesar:
            if columna in df.columns:
                df[columna] = pd.to_numeric(df[columna], errors='coerce')
        
        df = df.replace({np.nan: None})
        
        return df
    except Exception as e:
        print(f'Fallo la limpieza de finanzas operativas {e}')
        return df


# Función para limpiar los datos financieros de balanza
def clean_data_finanzas_balanza(df):
    try:
        columnas_a_procesar = [
            'MarketCap', 'TotalRevenue', 'NetIncomeToCommon', 'DebtToEquity', 'FreeCashflow'
        ]

        for columna in columnas_a_procesar:
            if columna in df.columns: 
                df[columna] = pd.to_numeric(df[columna], errors='coerce')
                if columna in ['MarketCap', 'TotalRevenue', 'NetIncomeToCommon', 'FreeCashflow']:
                    df[columna] = df[columna] / 1_000_000  
                    
        df = df.replace({np.nan: None})
        
        return df
    except Exception as e:
        print(f'Fallo la limpieza de finanzas balanza {e}')
        return df
    

# Función para limpiar los datos financieros de dividendos
def clean_data_finanzas_dividendos(df):
    try:
        columnas_a_procesar = [
            'DividendRate', 'DividendYield', 'PayoutRatio'
        ]

        for columna in columnas_a_procesar:
            if columna in df.columns:
                df[columna] = pd.to_numeric(df[columna], errors='coerce')
        
        df = df.replace({np.nan: None})
        
        return df
    except Exception as e:
        print(f'Fallo la limpieza de finanzas dividendos {e}')
        return df


# Creacion de la BBDD en MySQL
def creacion_bbdd(nasdaq_tickers_historic_clean, nasdaq_tickers_info_clean, finanzas_operativas_clean, finanzas_balanza_clean, finanzas_dividendos_clean,time_stamp_clean):
    try:
        initial_engine = get_engine()
        with initial_engine.connect() as connection:
            result = connection.execute(text("CREATE DATABASE IF NOT EXISTS yahoo_finance_nasdaq_100"))
            print("Base de datos 'yahoo_finance_nasdaq_100' creada/verificada con éxito.")
        
        # Conectarse a la base de datos 'yahoo_finance_nasdaq_100'
        engine = get_engine_database()
        with engine.connect() as connection:
            print("Conexión establecida con éxito a la base de datos yahoo_finance_nasdaq_100.")
    except Exception as e:
        print(f"Error al establecer la conexión: {e}")

    # Crea las tablas en la base de datos
    try:
        tablas.create_all(engine, checkfirst=True)
        print("Tablas creadas/verificadas con éxito.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

    # Asegura que Datetime solo se use date
    try:
        nasdaq_tickers_historic_clean['Date'] = pd.to_datetime(nasdaq_tickers_historic_clean['Date']).dt.date
        nasdaq_tickers_historic_clean["Cluster"] = None
        
        # Desactivar las restricciones de clave foránea temporalmente para el llenado
        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0;"))

        # Insertar/actualizar los datos en nasdaq_tickers_historic_sql
        try:
            with engine.begin() as conn:
                data = nasdaq_tickers_historic_clean.to_dict(orient='records')
                stmt = insert(tickers_historic_table).values(data)
                update_dict = {c.name: c for c in stmt.inserted if c.name not in ['Date', 'Ticker']}
                stmt = stmt.on_duplicate_key_update(update_dict)
                conn.execute(stmt)
            print("Datos insertados en nasdaq_tickers_historic_sql correctamente.")
        except Exception as e:
            print(f"Error al insertar datos en nasdaq_tickers_historic_sql: {e}")

        # Insertar/actualizar los datos en nasdaq_tickers_info_sql
        try:
            with engine.begin() as conn:
                data = nasdaq_tickers_info_clean.to_dict(orient='records')
                stmt = insert(tickers_info_table).values(data)
                update_dict = {c.name: c for c in stmt.inserted if c.name != 'Ticker'}
                stmt = stmt.on_duplicate_key_update(update_dict)
                conn.execute(stmt)
            print("Datos insertados en nasdaq_tickers_info_sql correctamente.")
        except Exception as e:
            print(f"Error al insertar datos en nasdaq_tickers_info_sql: {e}")

        # Insertar/actualizar los datos en las tablas de finanzas
        for table, data_clean, table_name in [
            (finanzas_operativas_table, finanzas_operativas_clean, "finanzas_operativas_sql"),
            (finanzas_balanza_table, finanzas_balanza_clean, "finanzas_balanza_sql"),
            (finanzas_dividendos_table, finanzas_dividendos_clean, "finanzas_dividendos_sql"),
        ]:
            try:
                with engine.begin() as conn:
                    data = data_clean.to_dict(orient='records')
                    stmt = insert(table).values(data)
                    update_dict = {c.name: c for c in stmt.inserted if c.name != 'Ticker'}
                    stmt = stmt.on_duplicate_key_update(update_dict)
                    conn.execute(stmt)
                print(f"Datos insertados en {table_name} correctamente.")
            except Exception as e:
                print(f"Error al insertar datos en {table_name}: {e}")

        # Insertar datos en la tabla `time_stamp_sql`
        try:
            with engine.begin() as conn:
                timestamp_value = time_stamp_clean.iloc[0, 0]
                stmt = insert(time_stamp_table).values({"TimestampExtraction": timestamp_value})
                stmt = stmt.on_duplicate_key_update({"TimestampExtraction": timestamp_value})
                conn.execute(stmt)
            print("TimestampExtraction insertado/actualizado correctamente en time_stamp_sql.")
        except Exception as e:
            print(f"Error al insertar/actualizar el timestamp en time_stamp_sql: {e}")
            raise e

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


# Obtener y limpiar info general de los tickers
try:
    informacion_tickers = obtener_informacion_tickers(tickers)
    nasdaq_tickers_info_clean = clean_data_info(informacion_tickers)
except Exception as e:
    print(f'Error en la llamada de info general: {e}')


# Obtener y limpiar las 3 métricas financieras
try:
    finanzas_operativas, finanzas_balanza, finanzas_dividendos = obtener_informacion_finanzas_tickers(tickers)

    finanzas_operativas_clean = clean_data_finanzas_operativas(finanzas_operativas)
    finanzas_balanza_clean = clean_data_finanzas_balanza(finanzas_balanza)
    finanzas_dividendos_clean = clean_data_finanzas_dividendos(finanzas_dividendos)
except Exception as e:
    print(f'Error en la llamada de métricas financieras: {e}')


# Obtener el df del timestamp 
try:
    time_stamp_clean = obtener_timestamp_actual()  
except Exception as e:
    print(f'Error al obtener el timestamp: {e}')


# Crear la bbdd y las tablas
try:
    creacion_bbdd(nasdaq_tickers_historic_clean, nasdaq_tickers_info_clean, finanzas_operativas_clean, finanzas_balanza_clean, finanzas_dividendos_clean,time_stamp_clean)
except Exception as e:
    print(f'No se creó la BBDD: {e}')

#Funcion para realizar el clustering
#try:
    #clustering_process(get_engine_database(), nasdaq_tickers_historic_clean)
#except Exception as e:
    #print(f'Error al realizar el clustering: {e}')

nasdaq_tickers_historic, nasdaq_tickers_info, timestamp = descargar_data_sql()


# Generamos los 3 df en formato CSV para powerBI
nasdaq_tickers_historic.to_csv("nasdaq_tickers_historic_clean.csv", index=False)
nasdaq_tickers_info.to_csv("nasdaq_tickers_info_clean.csv", index=False)
timestamp.to_csv("timestamp_data_clean.csv", index=False)
