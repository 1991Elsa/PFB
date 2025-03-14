import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
#from modules.clustering.tratamiento_nans_cluster import nasdaq_tickers_historic
from modules.MySQL.connect_engine import get_engine_database, get_engine
from modules.MySQL.tablas_metadata_5 import *
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import create_engine
from collections import Counter
from sklearn.metrics import silhouette_score
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

engine = get_engine_database()

def clustering_process(engine, df):
    """
    Ejecuta el modelo de clustering con un sampler aleatorio de 10,000 filas. 
    El modelo agrupa las acciones en función de su similitud o diferencia durante períodos de tiempo, con un enfoque basado en series temporales. 
    Este enfoque compara cómo evolucionan las acciones a lo largo del tiempo y las agrupa según su comportamiento temporal.
    Normaliza los datos usando StandardScaler y entrena el modelo DBSCAN. 
    Posteriormente, infiere los datos faltantes con randomforestclassifier en las filas donde no se generó cluster en el muestreo.
    Finalmente, la columna cluster se almacena en la tabla nasdaq_tickers_historic_sql de la base de datos yahoo_finance_nasdaq_100 en MySQL.

    Parámetro: Dataframe limpio con información historica de los tickers.

    Retorna: Dataframe con la columna "Cluster" que indica a qué cluster pertenece cada ticker.
    """

    try:
        
        features = ['Close', 'High', 'Low', 'Open']
        
        scaler = StandardScaler()
        df.loc[:, features] = scaler.fit_transform(df[features])
        
        random_indices = np.random.choice(df.index.values, size=10_000, replace=False)
        print(random_indices)
        

        dbscan = DBSCAN(eps= 1.8, min_samples= 10)
        df.loc[random_indices, 'Cluster'] = dbscan.fit_predict(df.loc[random_indices,features])

        clusters_labels = Counter(dbscan.labels_)
        print(clusters_labels)

        # Resultado de 0.98 es excelente y sugiere no cambiar eps ni minsample.  significa que el punto i está bien separado de otros clústeres y cercano a los puntos de su propio clúster. Esto indica una buena calidad de agrupación.
        sil_score = silhouette_score(df.loc[random_indices,features], dbscan.labels_)
        print("Silhouette Score:", sil_score)
        print("Finaliza clustering sampler")

    except Exception as e:
        print(f"Error en el proceso de clustering: {e}")
        raise e

        # Inferir los clusters faltantes en las filas donde no se generó en el muestreo con DBSCAN
    try:
        
        df_inferido = df[['Close', 'High', 'Low', 'Open', "Cluster"]]

        with_cluster = df_inferido.dropna(subset=["Cluster"]).copy()
        without_cluster = df_inferido[df_inferido["Cluster"].isna()].copy()

        X = with_cluster.drop(columns=["Cluster"])
        y = with_cluster["Cluster"].astype(int)

        X_prediction = without_cluster.drop(columns=["Cluster"])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        model.fit(X_train, y_train)

        y_prediction = model.predict(X_test)

        #print(classification_report(y_test, y_prediction))

        without_cluster["Cluster"] = model.predict(X_prediction)

        df_inferido = pd.concat([with_cluster, without_cluster], axis= 0).reset_index(drop=True)

        df = pd.concat([df_inferido, df[["Date", "Ticker", "Volume"]]], axis=1).reset_index(drop=True)
        orden_columnas = ["Date", "Ticker", "Close", "High", "Low", "Open", "Volume", "Cluster"]
        df = df[orden_columnas]

        print("Finaliza clustering inferido")

    except Exception as e:
        print(f'Fallo al inferir los clusters faltantes {e}')
        raise e
    
    try:
        # Using a context manager to handle the connection
        with engine.connect() as connection:
            # Begin a transaction
            with connection.begin() as transaction:
                try:
                    for index, row in df.dropna(subset="Cluster").iterrows():
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
        print(f"Error en la  actualización de base de datos: {e}")
        raise e

    return clusters_labels