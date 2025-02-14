import pandas as pd
from funcion_extraccion_info_historicos import nasdaq_tickers_historic

def roi(ticker, fecha_inicial, fecha_final, df = nasdaq_tickers_historic):
    """
    Calcula el ROI (Retorno de la Inversión) para un ticker específico en un período determinado.
    
    Parámetros:
    - ticker (str): Símbolo del ticker de la acción.
    - fecha_inicial (str): Fecha de inicio en formato 'YYYY-MM-DD'.
    - fecha_final (str): Fecha de fin en formato 'YYYY-MM-DD'.
    - df (DataFrame): DataFrame con los datos históricos, debe contener 'Date', 'Ticker' y 'Close'.
    
    Retorna:
    - ROI (%) como un valor float.
    """
 
    fecha_inicial = pd.to_datetime(fecha_inicial)
    fecha_final = pd.to_datetime(fecha_final)

    df_ticker = df[(df['Ticker'] == ticker) & (df['Date'].between(fecha_inicial, fecha_final))]

    # Verificar que haya datos suficientes
    if df_ticker.empty:
        return f"No hay datos disponibles para {ticker} en el período seleccionado."

    
    precio_inicial = df_ticker.iloc[0]['Close']
    precio_final = df_ticker.iloc[-1]['Close']

    # Verificar que los precios no sean NaN
    if pd.isna(precio_inicial) or pd.isna(precio_final):
        return f"No se pueden calcular valores de ROI debido a datos faltantes para {ticker}."

    
    roi_value = ((precio_final - precio_inicial) / precio_inicial) * 100

    return round(roi_value, 2)