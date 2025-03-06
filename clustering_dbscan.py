import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from descarga_sql import nasdaq_tickers_historic
from connect_engine import *
from tablas_metadata import *
from sqlalchemy.dialects.mysql import insert

"""
Para definir un algoritmo de clustering que agrupe acciones 
en función de su similitud o diferencia durante períodos de tiempo, 
podemos usar un enfoque basado en series temporales. 

Este enfoque compara cómo evolucionan las acciones a lo largo 
del tiempo y las agrupa según su comportamiento temporal.

Usaremos las series temporales de los precios historicos contenidos en 
nasdaq_tickers_historic 


"""

def clustering_process(engine, nasdaq_tickers_historic):

    try:
        # Seleccionar características para el clustering:

        features = ['Close', 'High', 'Low', 'Open']

        # Reemplazar NaN con la media de cada columna antes de normalizar
        nasdaq_tickers_historic[features] = nasdaq_tickers_historic[features].apply(lambda x: x.fillna(x.mean()), axis=0)
        
        
        # Normalizar los datos usando StandardScaler:

        scaler = StandardScaler()
        nasdaq_tickers_historic.loc[:, features] = scaler.fit_transform(nasdaq_tickers_historic[features])


        # Aplicar DBSCAN clustering:

        dbscan = DBSCAN(eps= 0.5, min_samples= 5)
        nasdaq_tickers_historic.loc[:, 'Cluster'] = dbscan.fit_predict(nasdaq_tickers_historic[features])

        #Mostrar algunos resultados para comprobar(dejar siempre comentada despues)
        #nasdaq_tickers_historic[['ticker', 'date', 'cluster']].head()


        # Crear el engine y conectar a la base de datos yahoo_finance
        engine = get_engine_database()

        # Verificar la conexión
        try:
            connection = engine.connect()
            connection.close()
            print("Conexión establecida con éxito a la base de datos yahoo_finance.")
        except Exception as e:
            print(f"Error al establecer la conexión: {e}")


        # Añadir la columna 'Cluster' a la estructura de la tabla si no existe:

        with engine.connect() as conn:
                conn.execute(text("""
                    ALTER TABLE nasdaq_tickers_historic_sql ADD COLUMN cluster INT;
                """))
            
        # Insertar/actualizar los valores en la base de datos
        with engine.begin() as conn:
            for index, row in nasdaq_tickers_historic.iterrows():
                stmt = text("""
                    UPDATE nasdaq_tickers_historic_sql 
                    SET cluster = :cluster 
                    WHERE ticker = :ticker AND date = :date
                """)
                conn.execute(stmt, {"cluster": int(row['Cluster']), "ticker": row['Ticker'], "date": row['Date']})
            
        print("Clustering actualizado en la base de datos correctamente.")
        

    except Exception as e:
        print(f"Error en el proceso de clustering: {e}")
    