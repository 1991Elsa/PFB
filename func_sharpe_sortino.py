import numpy as np
import pandas as pd
from funcion_extraccion_info_historicos import nasdaq_tickers_historic


def sharpe_ratio(ticker, start_date, end_date, df= nasdaq_tickers_historic, risk_free_rate=0.02):
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

    df_ticker['Rendimiento Diario'] = df_ticker['Close'].pct_change().dropna()

    if df_ticker['Rendimiento Diario'].dropna().empty:
        return f"No se pueden calcular rendimientos diarios para {ticker} en el período seleccionado."

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
'''
🏆 Cómo interpretar el Ratio de Sharpe

>1 → 🔥 Buena inversión ajustada al riesgo
>2 → 🚀 Excelente inversión
>3 → ⭐ Inversión excepcional
<1 → ⚠️ Riesgo alto en relación con el retorno


'''


def sortino_ratio(ticker, start_date, end_date, df= nasdaq_tickers_historic, risk_free_rate=0.02):
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

    
    df_ticker['Rendimiento Diario'] = df_ticker['Close'].pct_change()

    
    if df_ticker['Rendimiento Diario'].dropna().empty:
        return f"No se pueden calcular rendimientos diarios para {ticker} en el período seleccionado."

    
    mean_daily_return = df_ticker['Rendimiento Diario'].mean()

    # Convertir a base anualizada (252 días de mercado por año)
    mean_annual_return = mean_daily_return * 252

    # Calcular la desviación estándar solo de los rendimientos negativos
    downside_returns = df_ticker['Rendimiento Diario'][df_ticker['Rendimiento Diario'] < 0]
    downside_deviation = np.sqrt((downside_returns**2).sum() / len(downside_returns)) * np.sqrt(252)

    
    if downside_deviation == 0 or pd.isna(downside_deviation):
        return f"La volatilidad negativa es cero o no definida para {ticker}, por lo que no se puede calcular el Ratio de Sortino."

    
    sortino = (mean_annual_return - risk_free_rate) / downside_deviation

    return round(sortino, 2)
'''
🔍 ¿Cómo interpretar el Ratio de Sortino?

>1 → 🔥 Buena inversión ajustada al riesgo.
>2 → 🚀 Excelente inversión.
>3 → ⭐ Inversión excepcional.
<1 → ⚠️ Riesgo alto en relación con la rentabilidad.
Un Ratio de Sortino alto significa que el activo genera buenos retornos con pocas caídas.
'''



