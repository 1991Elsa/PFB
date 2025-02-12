
"""

En este script se define una funcion para extraer los diferentes datos de los 
componentes de índice bursátil NASDAQ - 100 y los del propio indice

Tengase en cuenta:

Indice bursátil: Nasdaq 100 (NQ=F)
Componentes: Listado de empresas (tickers_nasdaq)
Variables: Price	Close	High	Low	Open	Volume 

**Esta funcion sirve tanto cuando hacemos:

ticker = "NQ=F"
ticker = tikers_nasdaq

Devuelve un DataFrame se le puede hacer .head()

"""

def get_datos_historicos (ticker, start_date="2020-01-01"):

    end_date = datetime.now().strftime('%Y-%m-%d')

    datos = yf.download(ticker, start = start_date, end = end_date)

    return datos

def get_ticker_info (ticker):
    ticker_info = yf.Ticker(ticker).info
    return ticker_info