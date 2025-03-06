
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
#from tratamiento_nans import nasdaq_tickers_historic
#from encoding import df_info_encoded, industry_mapping

def modelo_clasification(df, target_colum):
    
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

#rf_model, scaler = modelo_clasificacion(nasdaq_tickers_historic, "cluster")
rf_model, scaler = modelo_clasification(df_info_encoded, "SectorEnergy")

print(rf_model)