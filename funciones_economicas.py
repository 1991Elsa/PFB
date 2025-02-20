import pandas as pd
import numpy as np

#funcion para sacar el ROI
def roi(ticker, fecha_inicial, fecha_final, df):
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

#funcion para sacar el ratio de sharpe
def sharpe_ratio(ticker, start_date, end_date, df, risk_free_rate=0.02):
    """
    Calcula el Ratio de Sharpe para un activo en base a un rango de fechas determinado.

    Parámetros:
    - ticker (str): Símbolo del ticker de la acción.
    - df (DataFrame): DataFrame con los datos históricos ('Date', 'Ticker', 'Close').
    - start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
    - end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.
    - risk_free_rate (float): Tasa libre de riesgo anualizada (por defecto 2% = 0.02).

    Retorna:
    - Ratio de Sharpe como un valor float.
    """
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df_ticker = df[(df['Ticker'] == ticker) & (df['Date'].between(start_date, end_date))].sort_values(by='Date')

    if df_ticker.shape[0] < 2:
        return f"No hay suficientes datos para calcular el Ratio de Sharpe de {ticker} en el período seleccionado."

    df_ticker['Rendimiento Diario'] = df_ticker['Close'].pct_change(fill_method=None)

    #if df_ticker['Rendimiento Diario'].dropna().empty:
    #    return f"No se pueden calcular rendimientos diarios para {ticker} en el período seleccionado."

    mean_daily_return = df_ticker['Rendimiento Diario'].mean()

    # Calcular la volatilidad (desviación estándar de los rendimientos diarios)
    std_dev_daily_return = df_ticker['Rendimiento Diario'].std()

    # Convertir a base anualizada (252 días de mercado por año)
    mean_annual_return = mean_daily_return * 252
    std_dev_annual_return = std_dev_daily_return * np.sqrt(252)

     
    if std_dev_annual_return == 0 or pd.isna(std_dev_annual_return):
        return f"La volatilidad es cero o no definida para {ticker}, por lo que no se puede calcular el Ratio de Sharpe."

     
    sharpe = (mean_annual_return - risk_free_rate) / std_dev_annual_return

    return round(sharpe, 2)

#funcion para sacar el ratio de sortino

def sortino_ratio(ticker, start_date, end_date, df, risk_free_rate=0.02):
    """
    Calcula el Ratio de Sortino para un activo en base a un rango de fechas determinado.

    Parámetros:
    - ticker (str): Símbolo del ticker de la acción.
    - df (DataFrame): DataFrame con los datos históricos ('Date', 'Ticker', 'Close').
    - start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
    - end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.
    - risk_free_rate (float): Tasa libre de riesgo anualizada (por defecto 2% = 0.02).

    Retorna:
    - Ratio de Sortino como un valor float.
    """

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df_ticker = df[(df['Ticker'] == ticker) & (df['Date'].between(start_date, end_date))].sort_values(by='Date')

    if df_ticker.shape[0] < 2:
        return f"No hay suficientes datos para calcular el Ratio de Sortino de {ticker} en el período seleccionado."

    df_ticker['Rendimiento Diario'] = df_ticker['Close'].pct_change(fill_method=None)

    mean_daily_return = df_ticker['Rendimiento Diario'].mean()
    mean_annual_return = mean_daily_return * 252

    # Filtrar solo los retornos negativos
    downside_returns = df_ticker['Rendimiento Diario'][df_ticker['Rendimiento Diario'] < 0]

    # Usar la desviación estándar correcta
    downside_deviation = downside_returns.std() * np.sqrt(252)

    if downside_deviation == 0 or pd.isna(downside_deviation):
        return f"La volatilidad negativa es cero o no definida para {ticker}, por lo que no se puede calcular el Ratio de Sortino."

    sortino = (mean_annual_return - risk_free_rate) / downside_deviation

    return round(sortino, 2)





#funcion para sacar la volatilidad
def calcular_volatilidad(df_nasdaq_tickers_historic_clean, periodo="diario"):
    """
    Calcula la volatilidad de los tickers del Nasdaq 100 usando la desviación estándar
    de los rendimientos diarios o mensuales.

    Parámetros:

    - df (DataFrame): DataFrame con los datos históricos ('Date', 'Ticker', 'Close').
    - periodo: "diario" o "mensual"

    Retorna:
    - DataFrame con la volatilidad de cada ticker.
    """

    # Convertir la columna 'Date' a tipo datetime
    df_nasdaq_tickers_historic_clean['Date'] = pd.to_datetime(df_nasdaq_tickers_historic_clean['Date'])

    # Calcular rendimientos diarios
    df_nasdaq_tickers_historic_clean['Rentabilidad'] = df_nasdaq_tickers_historic_clean.groupby('Ticker')['Close'].pct_change(fill_method=None)

    if periodo == "mensual":
        # Convertir las fechas al inicio del mes
        df_nasdaq_tickers_historic_clean['Month'] = df_nasdaq_tickers_historic_clean['Date'].dt.to_period('M')
        # Calcular la variación mensual de cierre
        datos_mensuales = df_nasdaq_tickers_historic_clean.groupby(['Ticker', 'Month'])['Close'].last().pct_change(fill_method=None)
        volatilidad = datos_mensuales.groupby('Ticker').std().reset_index()
    elif periodo == "diario":
        # Calcular la desviación estándar de los rendimientos diarios
        volatilidad = df_nasdaq_tickers_historic_clean.groupby('Ticker')['Rentabilidad'].std().reset_index()
    else:
        raise ValueError("El periodo debe ser 'diario' o 'mensual'.")

    volatilidad.columns = ['Ticker', 'Volatilidad']
    volatilidad = volatilidad.sort_values(by="Volatilidad", ascending=False).reset_index(drop=True)

    return volatilidad

#funcion para sacar la correlacion
def calcular_correlacion(df_nasdaq_tickers_historic_clean, periodo="diario"):
    """
    Calcula la correlación entre los activos usando sus rendimientos.

    Parámetros:
    - datos_historicos: DataFrame generado por get_datos_historicos()
    - periodo: "diario" o "mensual"

    Retorna:
    - Matriz de correlación de los activos seleccionados.
    """
    # Convertir la columna 'Date' a datetime
    df_nasdaq_tickers_historic_clean['Date'] = pd.to_datetime(df_nasdaq_tickers_historic_clean['Date'])

    # Filtrar solo los tickers seleccionados
    df_nasdaq_tickers_historic_clean = df_nasdaq_tickers_historic_clean[df_nasdaq_tickers_historic_clean['Ticker'].isin(df_nasdaq_tickers_historic_clean["Ticker"].unique().tolist())]
    
    # Calcular rendimientos diarios
    df_nasdaq_tickers_historic_clean['Rentabilidad'] = df_nasdaq_tickers_historic_clean.groupby('Ticker')['Close'].pct_change(fill_method=None)

    if periodo == "mensual":
        df_nasdaq_tickers_historic_clean['Month'] = df_nasdaq_tickers_historic_clean['Date'].dt.to_period('M')
        datos_mensuales = df_nasdaq_tickers_historic_clean.groupby(['Ticker', 'Month'])['Close'].last().pct_change()
        matriz_correlacion = datos_mensuales.unstack().corr()
    elif periodo == "diario":
        # Crear matriz de rendimientos diarios
        matriz_rentabilidades = df_nasdaq_tickers_historic_clean.pivot(index="Date", columns="Ticker", values="Rentabilidad")
        matriz_correlacion = matriz_rentabilidades.corr()
    else:
        raise ValueError("El periodo debe ser 'diario' o 'mensual'.")

    return matriz_correlacion
