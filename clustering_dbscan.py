import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from descarga_sql import nasdaq_tickers_historic
from connect_engine import *
from tablas_metadata import *
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import create_engine


"""
Para definir un algoritmo de clustering que agrupe acciones 
en función de su similitud o diferencia durante períodos de tiempo, 
podemos usar un enfoque basado en series temporales. 

Este enfoque compara cómo evolucionan las acciones a lo largo 
del tiempo y las agrupa según su comportamiento temporal.

Usaremos las series temporales de los precios historicos contenidos en 
nasdaq_tickers_historic 


"""

def clustering_process(nasdaq_tickers_historic):

    # Crear el engine y conectar a la base de datos yahoo_finance
    engine = get_engine_database()

    # with engine.connect() as connection:
    #     nasdaq_tickers_historic = pd.read_sql_table("nasdaq_tickers_historic_sql", con=connection)

    try:
        # Seleccionar características para el clustering:

        features = ['Close', 'High', 'Low', 'Open']

        # Reemplazar NaN con la media de cada columna antes de normalizar
        nasdaq_tickers_historic[features] = nasdaq_tickers_historic[features].apply(lambda x: x.fillna(x.mean()), axis=0)
        
        
        # Normalizar los datos usando StandardScaler:

        scaler = StandardScaler()
        nasdaq_tickers_historic.loc[:, features] = scaler.fit_transform(nasdaq_tickers_historic[features])

        # Sample
        random_indices = np.random.choice(nasdaq_tickers_historic.index.values, size=10_000, replace=False)
        print(random_indices)
        # Aplicar DBSCAN clustering:

        dbscan = DBSCAN(eps= 0.5, min_samples= 5)
        nasdaq_tickers_historic.loc[random_indices, 'Cluster'] = dbscan.fit_predict(nasdaq_tickers_historic.loc[random_indices,features])


        # Using a context manager to handle the connection
        with engine.connect() as connection:
            # Begin a transaction
            with connection.begin() as transaction:
                try:
                    for index, row in nasdaq_tickers_historic.dropna(subset="Cluster").iterrows():
                        stmt = text("""
                            UPDATE nasdaq_tickers_historic_sql 
                            SET cluster = :cluster 
                            WHERE ticker = :ticker AND date = :date
                        """)
                        connection.execute(stmt, {"cluster": int(row['Cluster']), "ticker": row['Ticker'], "date": row['Date']})
                    # If everything is successful, commit the transaction
                    transaction.commit()
                except Exception as e:
                    # If there is an error, rollback the transaction
                    transaction.rollback()
                    print(f"An error occurred: {e}")

                # Verificar la conexión
                try:
                    connection = engine.connect()
                    connection.close()
                    print("Conexión establecida con éxito a la base de datos yahoo_finance.")
                except Exception as e:
                    print(f"Error al establecer la conexión: {e}")

            
        print("Clustering actualizado en la base de datos correctamente.")
        

    except Exception as e:
        print(f"Error en el proceso de clustering: {e}")
        raise e

if __name__ == "__main__":
    print(nasdaq_tickers_historic.shape)
    clustering_process(nasdaq_tickers_historic)