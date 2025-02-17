

def calcular_correlacion(df_nasdaq_tickers_historic_clean, periodo="diario"):
    """
    Calcula la correlación entre los activos usando sus rendimientos.

    Parámetros:
    - datos_historicos: DataFrame generado por get_datos_historicos()
    - tickers: lista de tickers a analizar
    - periodo: "diario" o "mensual"

    Retorna:
    - Matriz de correlación de los activos seleccionados.
    """
    # Convertir la columna 'Date' a datetime
    df_nasdaq_tickers_historic_clean['Date'] = pd.to_datetime(df_nasdaq_tickers_historic_clean['Date'])

    # Filtrar solo los tickers seleccionados
    df_nasdaq_tickers_historic_clean = df_nasdaq_tickers_historic_clean[df_nasdaq_tickers_historic_clean['Ticker'].isin(tickers)]
    
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


"""
 Interpretación:

Valores cercanos a 1 → Se mueven juntos (ejemplo: AMZN y MSFT con 0.91).
Valores cercanos a 0 → No hay relación clara.
Valores negativos → Se mueven en direcciones opuestas.

"""