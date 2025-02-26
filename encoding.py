import pandas as pd
import numpy as np

import pickle
import sklearn
from sklearn.model_selection import KFold
import category_encoders as ce
from category_encoders.target_encoder import TargetEncoder

from descarga_sql import descargar_data_sql

nasdaq_tickers_historic, nasdaq_tickers_info = descargar_data_sql()

def encoding_fun(df):
    """
    Codifica las columnas categorícas en valores numéricos. 
    Utiliza Target encoding para la columna Industry y One Hot Encoding para las columnas Sector y Country. 

    Parámetro: Dataframe con todas las columnas

    Retorna: Dataframe codificado en archivo pickle.
    """

    df_info_encoded = pd.get_dummies(df, columns=["Sector", "Country"], dtype=int)

    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    industry_encoder = ce.TargetEncoder(cols=["Industry"])

    encoded_results =  []

    for train_index, val_index in kf.split(df_info_encoded):
        X_train, X_val = nasdaq_tickers_info.iloc[train_index], nasdaq_tickers_info.iloc[val_index]

        industry_encoder.fit(X_train["Industry"], X_train["MarketCap"])
        X_val_encoded = industry_encoder.transform(X_val["Industry"])

        encoded_results.append(X_val_encoded)

    encoded_df = pd.concat(encoded_results, ignore_index=True) 

    df_info_encoded["Industry_encoded"] = encoded_df

    pickle_file =df_info_encoded.to_pickle("df_info_encoded.pkl")

    return pickle_file


encoding_fun(nasdaq_tickers_info)


with open("df_info_encoded.pkl", "rb") as file:
   data = pickle.load(file)
print(data)
