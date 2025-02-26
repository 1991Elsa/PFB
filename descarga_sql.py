import pandas as pd
import numpy as np
import sklearn
from connect_engine import get_engine, get_engine_database  # Importar las funciones


def descargar_data_sql():
    # Crear el engine y conectar a la base de datos yahoo_finance
    engine = get_engine_database()

    # Verificar la conexión
    try:
        connection = engine.connect()
        connection.close()
        print("Conexión establecida con éxito a la base de datos yahoo_finance.")
    except Exception as e:
        print(f"Error al establecer la conexión: {e}")

    # Leer las tablas SQL en DataFrames de pandas
    try:
        df_historic = pd.read_sql_table(table_name="nasdaq_tickers_historic_sql", con=engine)
        df_info = pd.read_sql_table(table_name="nasdaq_tickers_info_sql", con=engine)
        df_finanzas = pd.read_sql_table(table_name="nasdaq_tickers_finanzas_sql", con=engine)
        print('Descarga de datos con exito')
        
       
    except Exception as e:
        print(f"Error al leer las tablas SQL: {e}")

    return df_historic, df_info, df_finanzas

nasdaq_tickers_historic, nasdaq_tickers_info, nasdaq_tickers_finanzas = descargar_data_sql()
