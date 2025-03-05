
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from tratamiento_nans_clasificacion import nasdaq_tickers_historic


def modelo_clasification(df, target_colum):
    """
    Filtra el dataframe nasdaq_tickers_historic para quedarse con los datos de los últimos dos años y poder correr el modelo de clasificación.
    Usa como target la columna "Cluster" que se obtiene del modelo de clustering de los últimos dos años.
    Normaliza los datos usando StandardScaler y entrena el modelo RandomForestClassifier.

    Parámetro: Dataframe limpio con información historica de los tickers y resultados del modelo de clustering.

    Retorna: Modelo de clasificación y escalador de datos con un accuracy de 0.9998
    """

    print(df.info())
    print(df.isna().sum())
    
    X = df.drop(columns=[target_colum])
    y = df[target_colum]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    with open('scaler_clasification.pkl', 'wb') as file:
        pickle.dump(scaler, file)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")

    with open('modelo_clasification.pkl', 'wb') as file:
        pickle.dump(rf_model, file)

    return rf_model, scaler

rf_model, scaler = modelo_clasification(nasdaq_tickers_historic, "Cluster")
