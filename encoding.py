import pandas as pd
import numpy as np

import pickle
import sklearn
from sklearn.model_selection import KFold
import category_encoders as ce
from category_encoders.target_encoder import TargetEncoder
from tratamiento_nans import nasdaq_tickers_info, nasdaq_tickers_historic


def encoding_fun_info(df):
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
        X_train, X_val = df.iloc[train_index], df.iloc[val_index]

        industry_encoder.fit(X_train["Industry"], X_train["MarketCap"])
        X_val_encoded = industry_encoder.transform(X_val["Industry"])

        encoded_results.append(X_val_encoded)

    encoded_df = pd.concat(encoded_results, ignore_index=True) 

    df_info_encoded["Industry_encoded"] = encoded_df

    industry_mapping = df_info_encoded.groupby("Industry")["MarketCap"].mean().to_dict()
    
    df_info_encoded.drop(columns=["Industry","Ticker","ShortName","Timestamp_extraction"], axis=1, inplace=True)

    df_info_encoded.columns = [col.replace("_", "") for col in df_info_encoded.columns]
    #print(df_info_encoded)

    df_info_encoded.to_pickle("df_info_encoded.pkl")

    return df_info_encoded, industry_mapping


df_info_encoded, industry_mapping = encoding_fun_info(nasdaq_tickers_info)


#with open("df_info_encoded.pkl", "rb") as file:
 #  data = pickle.load(file)
#print(data)

 #with open("industry_mapping.pkl", "wb") as file:
  #  pickle.dump(industry_mapping, file)
 #print(industry_mapping)

