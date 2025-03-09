import pandas as pd
import numpy as np
import sklearn
from connect_engine import get_engine_database
from datetime import datetime

def descargar_data_sql():
    engine = get_engine_database()
    try:
        connection = engine.connect()
        connection.close()
        print("Conexión establecida con éxito a la base de datos yahoo_finance.")
    except Exception as e:
        print(f"Error al establecer la conexión: {e}")
    # Lee las tablas SQL en df y cierra connect
    try:
        df_historic = pd.read_sql_table(table_name="nasdaq_tickers_historic_sql", con=engine)
        df_info = pd.read_sql_table(table_name="nasdaq_tickers_info_sql", con=engine)
        df_operativas = pd.read_sql_table(table_name="finanzas_operativas_sql", con=engine)
        df_balanza = pd.read_sql_table(table_name="finanzas_balanza_sql", con=engine)
        df_dividendos = pd.read_sql_table(table_name="finanzas_dividendos_sql", con=engine)
        df_timestamp = pd.read_sql_table(table_name="timestamp_sql", con=engine)
        print('Descarga de datos con exito')
    except Exception as e:
        print(f"Error al leer las tablas SQL: {e}")
    # Volvemos a juntar las 3 tablas de metricas financieras en df_info para manetener el código que ya teniamos.
    try:
        df_finanzas = pd.merge(df_operativas, df_balanza, on='Ticker')
        df_finanzas = pd.merge(df_finanzas, df_dividendos, on='Ticker')
        print('Union de las tablas de finanzas realizada con éxito')
    except Exception as e:
        print(f"Error al unir las tablas de finanzas: {e}")
    # Ahora unimos el df_finanzas al df_info
    try:
        df_info = pd.merge(df_info, df_finanzas, on='Ticker')
        print('Union de las tablas info y finanzas realizada con éxito')
    except Exception as e:
        print(f"Error al unir las tablas info y finanzas: {e}")
    return df_historic, df_info, df_timestamp

nasdaq_tickers_historic, nasdaq_tickers_info, timestamp = descargar_data_sql()


"""
En lugar de usar alchemy text y hacer las queries para descargar los datos de SQL como vamos a importar
las tablas completas, decidimos usar de pandas pd.read_sql ya que es mucho mas práctico.
query_historic = text("SELECT * FROM nasdaq_tickers_historic_sql")
query_info = text("SELECT * FROM nasdaq_tickers_info_sql")
"""






