import pandas as pd
import numpy as np

from sqlalchemy import create_engine
import sklearn
from config_engine import configuracion_engine

password, username, host, port = configuracion_engine("Dunidu")


engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/yahoo_finance")
connection = engine.connect()
connection.close()

df_historic = pd.read_sql_table(table_name="historic", con=engine)
df_info = pd.read_sql_table(table_name="information", con=engine)

print(df_historic)
print(df_info)