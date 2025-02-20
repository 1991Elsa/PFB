from connect_engine import *
from sqlalchemy import text, insert
import pandas as pd
import numpy as np
from tablas_metadata import *

# Creacion de la tabla en MySQL
def creacion_bbdd(df_info_clean, df_historic_clean):
    try:
        initial_engine = get_engine()
        with initial_engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión inicial establecida con éxito y librerías instaladas correctamente.")
        
        # Conectarse y crear la base de datos 'yahoo_finance' si no existe
        with initial_engine.connect() as connection:
            connection.execute(text("DROP DATABASE IF EXISTS yahoo_finance"))
            print("Base de datos 'yahoo_finance' eliminada con éxito.")
            connection.execute(text("CREATE DATABASE IF NOT EXISTS yahoo_finance"))
            print("Base de datos 'yahoo_finance' creada con éxito.")

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

nasdaq_tickers_info = pd.read_csv("nasdaq_tickers_info_clean.csv")
nasdaq_tickers_historic = pd.read_csv("nasdaq_tickers_historic_clean.csv")


creacion_bbdd(nasdaq_tickers_info, nasdaq_tickers_historic)