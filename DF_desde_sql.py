import pandas as pd
import numpy as np
import sklearn
from conect_engine import get_engine, get_engine_database 

# Crear el engine y conectar a la base de datos yahoo_finance
engine = get_engine_database()

# Verificar la conexión
try:
    connection = engine.connect()
    connection.close()
    print("Conexión establecida con éxito a la base de datos yahoo_finance.")
except Exception as e:
    print(f"Error al establecer la conexión: {e}")

# Realizar las consultas SQL para descargar los DataFrames
query_historic = "SELECT * FROM nasdaq_tickers_historic_sql"
query_info = "SELECT * FROM nasdaq_tickers_info_sql"

try:
    df_historic = pd.read_sql_query(query_historic, con=engine)
    df_info = pd.read_sql_query(query_info, con=engine)
    
    print("DataFrames descargados con éxito.")  

except Exception as e:
    print(f"Error al ejecutar las consultas SQL: {e}")
