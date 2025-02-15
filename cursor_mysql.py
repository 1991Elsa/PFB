import pandas as pd
import numpy as np

from sqlalchemy import create_engine

from funcion_extraccion_info_historicos import df_nasdaq_tickers_historic_clean
from funcion_extraccion_info_historicos import df_nasdaq_tickers_info_clean

DB_USER = "root"
DB_PASSWORD = "Dunidu"
DB_HOST ="localhost"
DB_NAME = "yahoo_finance"

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

def insert_data(df: pd.DataFrame, table_name: str, engine):
    if df.empty:
        print(f"No hay datos en el DataFrame para insertar a la tabla {table_name}.")
        return
    
    try:
        with engine.begin() as conn:
            df.to_sql(name=table_name, con=conn, if_exists="append",index=False)
        print(f"Anadidas {len(df)} filas en la tabla {table_name}")
    except Exception as e:
        print(f"Error al insertar datos en {table_name}: {e}")

from funcion_extraccion_info_historicos import df_nasdaq_tickers_historic_clean
from funcion_extraccion_info_historicos import df_nasdaq_tickers_info_clean

insert_data(df_nasdaq_tickers_historic_clean, "historic", engine)
insert_data(df_nasdaq_tickers_info_clean, "company_info", engine)
