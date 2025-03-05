import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from tratamiento_nans import nasdaq_tickers_historic
from connect_engine import get_engine_database
from tablas_metadata import *
from sqlalchemy.dialects.mysql import insert
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter


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


        # Seleccionar características para el clustering:

nasdaq_tickers_historic.drop(["Ticker", "Date"], axis=1, inplace=True)

X = nasdaq_tickers_historic.values

        # Normalizar los datos usando StandardScaler:

X_scaler = StandardScaler()
X = X_scaler.fit_transform(X)

        # Entrenar el modelo DBSCAN:

dbscan = DBSCAN(eps=0.20, min_samples=2*X.shape[1])
dbscan.fit(X)

Counter(dbscan.labels_)



