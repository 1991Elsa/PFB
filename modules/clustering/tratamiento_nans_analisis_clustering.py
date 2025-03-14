import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
#from modules.MySQL.descarga_sql import nasdaq_tickers_historic
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from plotly import express as px
from scipy.stats import skew, kurtosis
import pickle


def tratamiento_nans_historic_analisis(df):
    """
    Trata los valores nulos de la tabla nasdaq_tickers_historic previo al análisis de clusters. 
    Identifica la linealidad temporal de los datos y elimina los tickers que cumplen con esta característica; porque son 
    empresas que aún no habían entrado al mercado en el rango de fechas de la descarga. Para los tickers restantes, interpola los valores nulos.
    Cambia el tipo de datos de float64 a float32 para reducir el uso de memoria.
    Mantienen la estructura original de dataframe para poder hacer un análisis completo de los clusters.

    Parámetro: Dataframe con información historica de los tickers y resultados del modelo de clustering.

    Retorna: DataFrame limpio y sin valores nulos.
    """

    try:
        nans = df[df.isna().any(axis=1)]

        def verificar_linealidad_temporal(df):
            df["Date"] = pd.to_datetime(df["Date"])
            fechas = pd.date_range(start=df["Date"].min(), end=df["Date"].max(), freq="MS")
            return fechas.isin(df["Date"]).all()
        
        tickers_con_linealidad = (nans.groupby("Ticker").apply(verificar_linealidad_temporal).loc[lambda x: x].index.tolist())

        sin_linealidad_temporal = list(set(nans["Ticker"]) - set(tickers_con_linealidad))

        # Eliminar las filas en las que  el ticker está en la lista de linealidad temporal
        df = df[~df["Ticker"].isin(tickers_con_linealidad)].reset_index(drop=True)

        # Interpolar datos para los tickers sin linealidad temporal
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values(["Ticker", "Date"])

        for ticker in sin_linealidad_temporal:
            ticker_sin_linealidad = df["Ticker"] == ticker
            df.loc[ticker_sin_linealidad, ["Close", "High", "Low", "Open", "Volume"]] = (
            df.loc[ticker_sin_linealidad].set_index("Date")[["Close", "High", "Low", "Open", "Volume"]]
            .interpolate(method="time", limit_direction="both").values)

        df = df.reset_index(drop=True)

        col_to_float32 = ["Close", "High", "Low", "Open", "Volume"]
        df[col_to_float32] = df[col_to_float32].astype("float32")

        with open('modelo_clustering.pkl', 'wb') as file:
             pickle.dump(df, file)

        print("Finaliza tratamiento nans para análisis de clusters")

    except Exception as e:
        print(f'Fallo el tratamiento de nans historic {e}')
        raise e
    
    return df

def analisis_cluster(df):
    """
    Grafica los datos del Dataframe, calcula la volatilidad y hace un análisis estadístico de cada una de las columnas numéricas.
    Concluye en las características de los clusters basandose en la volatilidad y el volumen de acciones vendidos como el nivel de negociación.

    Parámetro: Dataframe con información historica de los tickers y resultados del modelo de clustering.

    Retorna: Conclusión con las características de los clusters formados
    """
   
    #try:

       # valid_clusters = sorted(df["Cluster"].dropna().unique())
       # valid_clusters = [c for c in valid_clusters if c != -1]

       # fig = px.scatter(df,
       #                 x="Date",
       #                 y="Ticker",
       #                 color="Cluster",
       #                 title="Cluster de acciones",
       #                 labels={
       #                                  "Date": "Fecha",
       #                                  "Ticker": "Ticker",
       #                                  "Cluster": "Cluster"
       #                                  "Cluster": "Cluster"
       #                 },
  
       #                 category_orders={"Cluster": valid_clusters},
       #                 hover_data=["Ticker","Date", "Cluster"]
       # )
                
       # fig.update_layout(
       #                 xaxis_title="Fecha",
       #                 yaxis_title="Ticker",
       #                 legend_title="Cluster",
       #                 showlegend=True
       #                 )
       # fig.show()

        #plt.figure(figsize=(12,6))
        #sns.histplot(data=df, x="Volume", hue="Cluster", bins=50, kde=True)
        #plt.xscale("log")
        #plt.title("Distribución de volumen por cluster")
        #plt.show()

        #plt.figure(figsize=(12,6))
        #sns.boxplot(x="Cluster", y="Close", data=df)
        #plt.title("Distribución de precio de cierre por cluster")
        #plt.show()
    
    #except Exception as e:
     #   print(f'Fallo en los gráficos de cluster {e}')

    try:
            
        df["Volatilidad"] = df["High"] - df["Low"]
        volatilidad_stats = df.groupby("Cluster")["Volatilidad"].describe()
        #print("Volatilidad por cluster")
        #print(volatilidad_stats)

        cluster_outliers = df["Cluster"].min()
        df_sin_outliers = df[df["Cluster"] != cluster_outliers]

        resultados = {}

        distribucion_cluster = df_sin_outliers["Cluster"].value_counts()
        resultados["Distribución de Clusters"] = distribucion_cluster.to_dict()

        estadisticas = df_sin_outliers.groupby("Cluster").agg({
            "Close" : ["mean", "std", "min", "max", "median", "quantile", skew, kurtosis],
            "High" : ["mean", "std", "min", "max", "median", "quantile", skew, kurtosis],
            "Low" : ["mean", "std", "min", "max", "median", "quantile", skew, kurtosis],
            "Open" : ["mean", "std", "min", "max", "median", "quantile", skew, kurtosis],
            "Volume" : ["mean", "std", "min", "max", "median", "quantile", skew, kurtosis],
            "Volatilidad" : ["mean", "std", "min", "max", "median", "quantile", skew, kurtosis]
        })

        resultados["Estadísticas por Cluster"] = estadisticas.to_dict()

        conclusiones = []
        for cluster in distribucion_cluster.index:
            count = distribucion_cluster[cluster]
            mean_price = estadisticas.loc[cluster, ("Close", "mean")]
            volatility = estadisticas.loc[cluster, ("Volatilidad", "mean")]
            volume = estadisticas.loc[cluster, ("Volume", "mean")]
            
            conclusion = f"El cluster {cluster} : contiene {count} valores.  El Precio promedio es: {mean_price:.2f}. "
            if volatility > df_sin_outliers["Volatilidad"].mean():
                conclusion += " Son acciones con alta volatilidad "
            else:
                conclusion += " Son acciones con baja volatilidad  "
            if volume > df_sin_outliers["Volume"].mean():
                conclusion += " y alto volumen de negociación "
            else:
                conclusion += " y bajo volumen de negociación "
            conclusiones.append(conclusion)

        resultados["Conclusiones"] = conclusiones

        with open('resultados_cluster.pkl', 'wb') as file:
             pickle.dump(resultados, file)

    except Exception as e:
        print(f'Fallo en el análisis de cluster {e}')

    return resultados


