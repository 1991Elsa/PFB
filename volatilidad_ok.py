def calcular_volatilidad(df_nasdaq_tickers_historic_clean, periodo="diario"):
    """
    Calcula la volatilidad de los tickers del Nasdaq 100 usando la desviación estándar
    de los rendimientos diarios o mensuales.

    Parámetros:
    - ticker (str): Símbolo del ticker de la acción.
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

# Calcular volatilidad diaria
volatilidad_diaria = calcular_volatilidad(df_nasdaq_tickers_historic_clean, periodo="diario")
print(volatilidad_diaria)

# Calcular volatilidad mensual
volatilidad_mensual = calcular_volatilidad(df_nasdaq_tickers_historic_clean, periodo="mensual")
print(volatilidad_mensual)