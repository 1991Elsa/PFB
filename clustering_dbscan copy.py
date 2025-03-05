import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from tratamiento_nans_cluster import nasdaq_tickers_historic
from connect_engine import get_engine_database
from tablas_metadata import *
from sqlalchemy.dialects.mysql import insert
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter
import plotly.express as px



engine = get_engine_database()

def clustering_process(engine, nasdaq_tickers_historic):
        """
        Filtra el dataframe nasdaq_tickers_historic para quedarse con los datos de los últimos dos años y poder correr el modelo de clustering.
        Con el objetico de agrupar las acciones en función de su similitud o diferencia durante períodos de tiempo, con un enfoque basado en series temporales. 
        Este enfoque compara cómo evolucionan las acciones a lo largo del tiempo y las agrupa según su comportamiento temporal.
        Normaliza los datos usando StandardScaler y entrena el modelo DBSCAN.

        Parámetro: Dataframe limpio con información historica de los tickers.

        Retorna: Dataframe con la columna "Cluster" que indica a qué cluster pertenece cada ticker.
        """
        
        try:

                date = nasdaq_tickers_historic["Date"].max() - pd.DateOffset(years=2)
                nasdaq_tickers_historic = nasdaq_tickers_historic[nasdaq_tickers_historic["Date"] >= date].copy()


                tickers_dates = nasdaq_tickers_historic[["Ticker", "Date"]].copy()
                
                nasdaq_tickers_historic.drop(["Ticker", "Date"], axis=1, inplace=True)

                X = nasdaq_tickers_historic.values

                        # Normalizar los datos usando StandardScaler:

                X_scaler = StandardScaler()
                X = X_scaler.fit_transform(X)

                        # Entrenar el modelo DBSCAN:

                dbscan = DBSCAN(eps=0.20, min_samples=2*X.shape[1])
                dbscan.fit(X)

                print(Counter(dbscan.labels_))

                nasdaq_tickers_historic["Cluster"] = dbscan.labels_


                nasdaq_tickers_historic = pd.concat([tickers_dates, nasdaq_tickers_historic], axis=1)

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
                        check_cluster = text(""" 
                                SELECT COLUMN_NAME
                                FROM INFORMATION_SCHEMA.COLUMNS
                                WHERE TABLE_NAME = 'nasdaq_tickers_historic_sql' AND COLUMN_NAME = 'Cluster';
                                """)
                        result = conn.execute(check_cluster).fetchone()
                        if not result:
                                conn.execute(text("""
                                ALTER TABLE nasdaq_tickers_historic_sql ADD COLUMN Cluster INT;
                                """  ))
                
                # Insertar/actualizar los valores en la base de datos
                with engine.begin() as conn:
                        for _, row in nasdaq_tickers_historic.iterrows():
                                stmt = text("""
                                UPDATE nasdaq_tickers_historic_sql 
                                SET Cluster = :cluster
                                WHERE Ticker = :ticker AND Date = :date
                                """)
                                conn.execute(stmt, {"cluster": int(row['Cluster']), "ticker": row['Ticker'], "date": row['Date']})
                        
                print("Clustering actualizado en la base de datos correctamente.")

                fig = px.scatter(nasdaq_tickers_historic,
                                 x="Date",
                                 y="Ticker",
                                 color="Cluster",
                                 title="Cluster de acciones",
                                 labels={
                                         "Date": "Fecha",
                                         "Ticker": "Ticker",
                                         "Cluster": "Cluster"
                                 },
                                 category_orders={"Cluster": sorted(nasdaq_tickers_historic["Cluster"].unique())},
                                 hover_data=["Ticker","Date", "Cluster"])
                
                fig.update_layout(
                        xaxis_title="Fecha",
                        yaxis_title="Ticker",
                        legend_title="Cluster",
                        showlegend=True
                )
                fig.show()

        
        except Exception as e:
                print(f"Error en el proceso de clustering: {e}")


nasdaq_tickers_historic = clustering_process(engine, nasdaq_tickers_historic)



