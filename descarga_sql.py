import pandas as pd
import numpy as np
import sklearn
from connect_engine import get_engine_database 


def descargar_data_sql():
    # Crea el engine y se conecta a la base de datos yahoo_finance
    engine = get_engine_database()

    # Verifica la conexión
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
        df_finanzas = pd.read_sql_table(table_name="nasdaq_tickers_finanzas_sql", con=engine)
        print('Descarga de datos con exito')   
    except Exception as e:
        print(f"Error al leer las tablas SQL: {e}")

    # Volvemos a juntar las tablas separadas en df_info para manetener el código que ya teniamos.
    try:
        df_info = pd.merge(df_info, df_finanzas, on='Ticker')
        print('Merge de info+finanzas realizada con éxito')
    except Exception as e:
        print(f"Error al unificar info+finanzas: {e}")

    return df_historic, df_info

nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

"""
En lugar de usar alchemy text y hacer las queries para descargar los datos de SQL cya que vamos a importar 
las tablas completas, decidimos usar de pandas pd.read_sql ya que es mucho mas práctico.

query_historic = text("SELECT * FROM nasdaq_tickers_historic_sql")
query_info = text("SELECT * FROM nasdaq_tickers_info_sql")
query_finanzas = text("SELECT * FROM nasdaq_tickers_finanzas_sql")

"""