import pandas as pd
import sklearn

from sqlalchemy import create_engine, text
from funcion_extraccion_info_historicos import df_nasdaq_tickers_historic_clean, df_nasdaq_tickers_info_clean
from config_engine import configuracion_engine

password, username, host, port = configuracion_engine()

try:
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/")
    with engine.connect() as connection:
        connection.execute(text("CREATE DATABASE IF NOT EXISTS yahoo_finance"))
        print("Base de datos creada con exito")

    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/yahoo_finance")

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexión establecida con éxito a la base de datos")

    df_nasdaq_tickers_info_clean.to_sql(name="information", con=engine, if_exists="replace", index=False)
    df_nasdaq_tickers_historic_clean.to_sql(name="historic", con=engine, if_exists="replace", index=False)
    print("Tablas creadas con éxito.")

except Exception as e:
    print(f"Error al establecer la conexión: {e}")
