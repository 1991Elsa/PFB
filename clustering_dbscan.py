import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from tratamiento_nans_cluster import nasdaq_tickers_historic
from connect_engine import get_engine_database, get_engine
from tablas_metadata import *
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import create_engine
from collections import Counter
from sklearn.metrics import silhouette_score

engine = get_engine_database()

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

    # Crear el engine y conectar a la base de datos yahoo_finance
    engine = get_engine_database()

    # with engine.connect() as connection:
    #     nasdaq_tickers_historic = pd.read_sql_table("nasdaq_tickers_historic_sql", con=connection)

    try:
        # Seleccionar características para el clustering:

        features = ['Close', 'High', 'Low', 'Open']

        # Normalizar los datos usando StandardScaler:

        scaler = StandardScaler()
        nasdaq_tickers_historic.loc[:, features] = scaler.fit_transform(nasdaq_tickers_historic[features])

        # Sample
        random_indices = np.random.choice(nasdaq_tickers_historic.index.values, size=10_000, replace=False)
        print(random_indices)
        # Aplicar DBSCAN clustering:

        dbscan = DBSCAN(eps= 1.8, min_samples= 10)
        nasdaq_tickers_historic.loc[random_indices, 'Cluster'] = dbscan.fit_predict(nasdaq_tickers_historic.loc[random_indices,features])

        clusters_labels = Counter(dbscan.labels_)
        print(clusters_labels)

        # Resultado de 0.98 es excelente y sugiere no cambiar eps ni minsample.  significa que el punto i está bien separado de otros clústeres y cercano a los puntos de su propio clúster. Esto indica una buena calidad de agrupación.
        sil_score = silhouette_score(nasdaq_tickers_historic.loc[random_indices,features], dbscan.labels_)
        print("Silhouette Score:", sil_score)

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

    return clusters_labels

if __name__ == "__main__":

 modelo_clustering = clustering_process(engine, nasdaq_tickers_historic)