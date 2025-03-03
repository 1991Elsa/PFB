from sqlalchemy import MetaData, Table, Column, String, Float, DateTime, Date, ForeignKey, text, insert

tablas = MetaData()

tickers_historic_table = Table('nasdaq_tickers_historic_sql', tablas,
    Column('Date', Date, primary_key=True),
    Column('Ticker', String(10), ForeignKey('nasdaq_tickers_info_sql.Ticker'), primary_key=True),    
    Column('Close', Float),
    Column('High', Float),
    Column('Low', Float),
    Column('Open', Float),
    Column('Volume', Float)
)

tickers_info_table = Table('nasdaq_tickers_info_sql', tablas,
    Column('Ticker', String(10), primary_key=True),
    Column('ShortName', String(100)),
    Column('Sector', String(50)),
    Column('Industry', String(50)),
    Column('Country', String(50)),
    Column('Timestamp_extraction', DateTime)
)

finanzas_operativas_table = Table('finanzas_operativas_sql', tablas,
    Column('Ticker', String(10), ForeignKey('nasdaq_tickers_info_sql.Ticker'), primary_key=True),
    Column('ReturnOnAssets', Float),
    Column('ReturnOnEquity', Float),
    Column('OperatingMargins', Float),
    Column('GrossMargins', Float),
    Column('ProfitMargins', Float),
    Column('ebitdaMargins', Float)    
)

finanzas_balanza_table = Table('finanzas_balanza_sql', tablas,
    Column('Ticker', String(10), ForeignKey('nasdaq_tickers_info_sql.Ticker'), primary_key=True),
    Column('MarketCap', Float),
    Column('TotalRevenue', Float),
    Column('NetIncomeToCommon', Float),
    Column('DebtToEquity', Float),
    Column('FreeCashflow', Float)
)

finanzas_dividendos_table = Table('finanzas_dividendos_sql', tablas,
    Column('Ticker', String(10), ForeignKey('nasdaq_tickers_info_sql.Ticker'), primary_key=True),
    Column('DividendRate', Float),
    Column('DividendYield', Float),
    Column('PayoutRatio', Float)
)

time_stamp_table= Table('timestamp_sql', tablas,
    Column('Timestamp', DateTime, primary_key=True)
)










































import yfinance as yf

# Define el ticker que quieres analizar (puedes cambiarlo por cualquier otro de la lista)
ticker_symbol = 'AAPL'  # Ejemplo con Apple Inc.

# Obtén el objeto Ticker
ticker = yf.Ticker(ticker_symbol)

# Extrae la información completa
ticker_info = ticker.info

# Muestra la información
for key, value in ticker_info.items():
    print(f"{key}: {value}")

# esta es toda la informacion que se puede conseguir de cada ticker, aqui ejemplo APPL
"""

address1: One Apple Park Way  # Dirección de la sede principal de la empresa.
city: Cupertino  # Ciudad donde se encuentra la sede principal.
state: CA  # Estado donde se encuentra la sede principal.
zip: 95014  # Código postal de la sede principal.
country: United States  # País donde se encuentra la sede principal.
phone: (408) 996-1010  # Número de teléfono de contacto de la empresa.
website: https://www.apple.com  # Sitio web oficial de la empresa.
industry: Consumer Electronics  # Industria en la que opera la empresa.
industryKey: consumer-electronics  # Clave de la industria.
industryDisp: Consumer Electronics  # Descripción de la industria.
sector: Technology  # Sector industrial de la empresa.
sectorKey: technology  # Clave del sector.
sectorDisp: Technology  # Descripción del sector.
longBusinessSummary: Apple Inc. designs, manufactures, and markets smartphones, ...  # Resumen largo del negocio de la empresa.
fullTimeEmployees: 150000  # Número de empleados a tiempo completo.
companyOfficers: [{'maxAge': 1, 'name': 'Mr. Timothy D. Cook', 'age': 63, ...}]  # Información sobre los principales oficiales de la empresa.
auditRisk: 3  # Riesgo de auditoría.
boardRisk: 1  # Riesgo del consejo de administración.
compensationRisk: 3  # Riesgo de compensación.
shareHolderRightsRisk: 1  # Riesgo de derechos de los accionistas.
overallRisk: 1  # Riesgo general.
governanceEpochDate: 1738368000  # Fecha de la gobernanza en formato epoch.
compensationAsOfEpochDate: 1703980800  # Fecha de compensación en formato epoch.
irWebsite: http://investor.apple.com/  # Sitio web de relaciones con inversores.
executiveTeam: []  # Información sobre el equipo ejecutivo.
maxAge: 86400  # Máxima edad de la información en segundos.
priceHint: 2  # Indicador de precio.
previousClose: 247.1  # Precio de cierre anterior.
open: 248.0  # Precio de apertura del día.
dayLow: 244.91  # Precio más bajo del día.
dayHigh: 249.98  # Precio más alto del día.
regularMarketPreviousClose: 247.1  # Precio de cierre anterior en el mercado regular.
regularMarketOpen: 248.0  # Precio de apertura en el mercado regular.
regularMarketDayLow: 244.91  # Precio más bajo del día en el mercado regular.
regularMarketDayHigh: 249.98  # Precio más alto del día en el mercado regular.
dividendRate: 1.0  # Tasa de dividendo anual.
dividendYield: 0.4  # Rendimiento del dividendo en porcentaje.
exDividendDate: 1739145600  # Fecha ex-dividendo en formato epoch.
payoutRatio: 0.1571  # Índice de pago de dividendos.
fiveYearAvgDividendYield: 0.6  # Rendimiento promedio de dividendos de cinco años.
beta: 1.2  # Beta del stock, que mide la volatilidad en comparación con el mercado.
trailingPE: 39.212696  # Relación precio-beneficio (PE) histórica.
forwardPE: 29.728037  # Relación precio-beneficio (PE) futura estimada.
volume: 46872348  # Volumen de acciones negociadas en el día.
regularMarketVolume: 46872348  # Volumen de acciones negociadas en el mercado regular.
averageVolume: 50169216  # Volumen promedio de acciones negociadas.
averageVolume10days: 45929720  # Volumen promedio de acciones negociadas en los últimos 10 días.
averageDailyVolume10Day: 45929720  # Volumen promedio diario de acciones negociadas en los últimos 10 días.
bid: 235.2  # Precio de compra más alto.
ask: 260.4  # Precio de venta más bajo.
bidSize: 1  # Tamaño de la oferta de compra.
askSize: 1  # Tamaño de la oferta de venta.
marketCap: 3711059623936  # Capitalización de mercado total.
fiftyTwoWeekLow: 164.08  # Precio más bajo en las últimas 52 semanas.
fiftyTwoWeekHigh: 260.1  # Precio más alto en las últimas 52 semanas.
priceToSalesTrailing12Months: 9.377046  # Relación precio-ventas histórica de 12 meses.
fiftyDayAverage: 240.6826  # Promedio de precios en los últimos 50 días.
twoHundredDayAverage: 225.0356  # Promedio de precios en los últimos 200 días.
trailingAnnualDividendRate: 0.99  # Tasa anual de dividendo histórica.
trailingAnnualDividendYield: 0.004006475  # Rendimiento anual de dividendo histórico.
currency: USD  # Moneda en la que se negocian las acciones.
tradeable: False  # Indicador de si el stock es negociable.
enterpriseValue: 3754076930048  # Valor empresarial.
profitMargins: 0.24295  # Márgenes de beneficio.
floatShares: 14998187904  # Número de acciones flotantes.
sharesOutstanding: 15022100480  # Número total de acciones en circulación.
sharesShort: 124917523  # Número de acciones vendidas en corto.
sharesShortPriorMonth: 157008120  # Número de acciones vendidas en corto el mes anterior.
sharesShortPreviousMonthDate: 1735603200  # Fecha del mes anterior en formato epoch.
dateShortInterest: 1738281600  # Fecha de interés corto en formato epoch.
sharesPercentSharesOut: 0.0083  # Porcentaje de acciones en corto sobre el total de acciones en circulación.
heldPercentInsiders: 0.02286  # Porcentaje de acciones en manos de personas con información privilegiada (insiders).
heldPercentInstitutions: 0.62709  # Porcentaje de acciones en manos de instituciones financieras.
shortRatio: 2.12  # Relación de las acciones en corto en relación con el volumen promedio diario de negociación.
shortPercentOfFloat: 0.0083  # Porcentaje de acciones en corto en relación con las acciones flotantes.
impliedSharesOutstanding: 15390999552  # Número de acciones en circulación implícitas.
bookValue: 4.438  # Valor en libros por acción.
priceToBook: 55.66471  # Relación precio-valor en libros.
lastFiscalYearEnd: 1727481600  # Fecha de finalización del último año fiscal en formato epoch.
nextFiscalYearEnd: 1759017600  # Fecha de finalización del próximo año fiscal en formato epoch.
mostRecentQuarter: 1735344000  # Fecha del trimestre más reciente reportado en formato epoch.
earningsQuarterlyGrowth: 0.071  # Crecimiento trimestral de las ganancias.
netIncomeToCommon: 96150003712  # Ingreso neto atribuible a los accionistas comunes.
trailingEps: 6.3  # Ganancias por acción (EPS) de los últimos doce meses.
forwardEps: 8.31  # Ganancias por acción (EPS) estimadas para los próximos doce meses.
lastSplitFactor: 4:1  # Factor del último split de acciones.
lastSplitDate: 1598832000  # Fecha del último split de acciones en formato epoch.
enterpriseToRevenue: 9.486  # Relación entre el valor de la empresa y los ingresos.
enterpriseToEbitda: 27.332  # Relación entre el valor de la empresa y el EBITDA.
52WeekChange: 0.36170208  # Cambio porcentual en el precio de la acción en las últimas 52 semanas.
SandP52WeekChange: 0.17466116  # Cambio porcentual en el índice S&P 500 en las últimas 52 semanas.
lastDividendValue: 0.25  # Valor del último dividendo pagado por acción.
lastDividendDate: 1739145600  # Fecha del último dividendo pagado en formato epoch.
quoteType: EQUITY  # Tipo de cotización (acción).
currentPrice: 247.04  # Precio actual de la acción.
targetHighPrice: 325.0  # Precio objetivo más alto según los analistas.
targetLowPrice: 197.0  # Precio objetivo más bajo según los analistas.
targetMeanPrice: 252.22575  # Precio objetivo promedio según los analistas.
targetMedianPrice: 257.5  # Precio objetivo mediano según los analistas.
recommendationMean: 2.06522 # Promedio de las recomendaciones de los analistas (por ejemplo, compra, venta, mantener).
recommendationKey: buy # La recomendación principal de los analistas (por ejemplo, buy significa comprar).
numberOfAnalystOpinions: 40 # Número de opiniones de analistas sobre la acción.
totalCash: 53774999552 # El total de efectivo en posesión de la empresa.
totalCashPerShare: 3.58 # El total de efectivo por acción.
ebitda: 137352003584 # El EBITDA (beneficio antes de intereses, impuestos, depreciación y amortización).
totalDebt: 96798998528 # El total de deuda en posesión de la empresa.
quickRatio: 0.783 # La relación rápida, que mide la capacidad de una empresa para pagar sus pasivos a corto plazo con sus activos más líquidos.
currentRatio: 0.923 # La relación corriente, que mide la capacidad de una empresa para pagar sus pasivos a corto plazo con sus activos corrientes.
totalRevenue: 395760009216 # Los ingresos totales generados por la empresa en un período específico.
debtToEquity: 145.0 # La relación deuda-capital, que mide la proporción de deuda en relación con el capital propio de la empresa.
revenuePerShare: 25.974 # Los ingresos por acción, que se obtienen dividiendo los ingresos totales por el número de acciones en circulación.
returnOnAssets: 0.22518998 # El rendimiento sobre los activos (ROA), que mide cuán eficiente es una empresa para generar ganancias a partir de sus activos.
returnOnEquity: 1.3652 # El rendimiento sobre el patrimonio (ROE), que mide la rentabilidad generada sobre los fondos propios de la empresa.
grossProfits: 184102993920 # Los beneficios brutos de la empresa, que se obtienen restando el costo de los bienes vendidos de los ingresos totales.
freeCashflow: 93833871360 # El flujo de caja libre, que representa el efectivo que una empresa genera después de considerar los gastos de capital necesarios para mantener y expandir su base de activos.
operatingCashflow: 108293996544 # El flujo de caja operativo, que representa el efectivo generado por las operaciones normales de la empresa.
earningsGrowth: 0.101 # El crecimiento de las ganancias en un período específico en comparación con el período anterior.
revenueGrowth: 0.04 # El crecimiento de los ingresos en un período específico en comparación con el período anterior.
grossMargins: 0.46519002 # El margen bruto, que mide la eficiencia de una empresa para producir bienes o servicios en relación con sus ingresos netos.
ebitdaMargins: 0.34706002 # El margen de EBITDA, que mide la rentabilidad operativa de una empresa antes de considerar los costos financieros y fiscales.
operatingMargins: 0.34459 # El margen operativo, que mide la eficiencia operativa de una empresa al comparar las ganancias operativas con los ingresos.
financialCurrency: USD # La moneda en la que se reportan los estados financieros.
symbol: AAPL # El símbolo de cotización (ticker) de la empresa.
language: en-US # El idioma en el que se presenta la información.
region: US # La región en la que se cotiza la acción.
typeDisp: Equity # El tipo de cotización (en este caso, Equity indica que es una acción).
quoteSourceName: Nasdaq Real Time Price # La fuente de la cotización (en este caso, Nasdaq Real Time Price).
triggerable: True # Indica si la cotización puede activar alertas de precios.
customPriceAlertConfidence: HIGH # La confianza en las alertas de precios personalizadas.
regularMarketChangePercent: -0.024286853 # El cambio porcentual en el precio de la acción en el mercado regular.
regularMarketPrice: 247.04 # El precio de la acción en el mercado regular.
marketState: PRE # El estado del mercado (por ejemplo, PRE indica que el mercado está en premercado).
corporateActions: [] # Las acciones corporativas recientes (puede estar vacío).
preMarketTime: 1740578836 # La marca de tiempo del premercado.
regularMarketTime: 1740517200 # La marca de tiempo del mercado regular.
exchange: NMS # El intercambio en el que se cotiza la acción (en este caso, NMS indica Nasdaq).
messageBoardId: finmb_24937 # El ID del foro de mensajes para la acción.
exchangeTimezoneName: America/New_York # El nombre de la zona horaria del intercambio.
exchangeTimezoneShortName: EST # El nombre corto de la zona horaria del intercambio.
gmtOffSetMilliseconds: -18000000 # El desfase horario en milisegundos respecto al GMT.
market: us_market # El mercado en el que se cotiza la acción (en este caso, us_market indica el mercado de EE. UU.).
esgPopulated: False # Indica si la información ESG está disponible (puede estar vacío).
shortName: Apple Inc. # El nombre corto de la empresa.
longName: Apple Inc. # El nombre completo de la empresa.
hasPrePostMarketData: True # Indica si la acción tiene datos de premercado y postmercado.
firstTradeDateMilliseconds: 345479400000 # La fecha de la primera transacción en milisegundos desde 1970.
preMarketChange: -1.4299927 # El cambio en el precio de la acción en el premercado.
preMarketChangePercent: -0.5788507 # El cambio porcentual en el precio de la acción en el premercado.
preMarketPrice: 245.61 # El precio de la acción en el premercado.
regularMarketChange: -0.060012817 # El cambio en el precio de la acción en el mercado regular.
regularMarketDayRange: 244.91 - 249.98 # El rango diario de precios de la acción en el mercado regular.
fullExchangeName: NasdaqGS # El nombre completo del intercambio.
averageDailyVolume3Month: 50169216 # El volumen promedio diario de negociación en los últimos 3 meses.
fiftyTwoWeekLowChange: 82.95999 # El cambio en el precio de la acción desde el mínimo de 52 semanas.
fiftyTwoWeekLowChangePercent: 0.50560695 # El cambio porcentual en el precio de la acción desde el mínimo de 52 semanas.
fiftyTwoWeekRange: 164.08 - 260.1 # El rango de precios de la acción en las últimas 52 semanas.
fiftyTwoWeekHighChange: -13.060013 # El cambio en el precio de la acción desde el máximo de 52 semanas.
fiftyTwoWeekHighChangePercent: -0.050211504 # El cambio porcentual en el precio de la acción desde el máximo de 52 semanas.
fiftyTwoWeekChangePercent: 36.170208 # El cambio porcentual en el precio de la acción en las últimas 52 semanas.
dividendDate: 1739404800 # La fecha del próximo pago de dividendos.
earningsTimestamp: 1738272600 # La marca de tiempo de la última presentación de ganancias.
earningsTimestampStart: 1746010740 # La marca de tiempo de inicio de la próxima presentación de ganancias.
earningsTimestampEnd: 1746446400 # La marca de tiempo de finalización de la próxima presentación de ganancias.
earningsCallTimestampStart: 1738274400 # La marca de tiempo de inicio de la última llamada de ganancias.
earningsCallTimestampEnd: 1738274400 # La marca de tiempo de finalización de la última llamada de ganancias.
isEarningsDateEstimate: True # Indica si la fecha de ganancias es una estimación.
epsTrailingTwelveMonths: 6.3 # Las ganancias por acción (EPS) de los últimos doce meses.
epsForward: 8.31 # Las ganancias por acción (EPS) esperadas para los próximos doce meses.
epsCurrentYear: 7.33658 # Las ganancias por acción (EPS) esperadas para el año actual.
priceEpsCurrentYear: 33.672363 # La relación precio-EPS para el año.
fiftyDayAverageChange: 6.3573914 # Cambio en el precio promedio de los últimos 50 días.
fiftyDayAverageChangePercent: 0.026414005 # Cambio porcentual en el precio promedio de los últimos 50 días.
twoHundredDayAverageChange: 22.004395 # Cambio en el precio promedio de los últimos 200 días.
twoHundredDayAverageChangePercent: 0.09778184 # Cambio porcentual en el precio promedio de los últimos 200 días.
sourceInterval: 15 # Intervalo de la fuente en minutos para la actualización de datos.
exchangeDataDelayedBy: 0 # Tiempo de retraso en la actualización de los datos del intercambio en segundos.
averageAnalystRating: 2.1 - Buy # Promedio de la calificación de los analistas (por ejemplo, 2.1 indica una recomendación de compra).
cryptoTradeable: False # Indica si el activo es negociable en criptomonedas (False significa que no lo es).
displayName: Apple # Nombre para mostrar de la empresa.
trailingPegRatio: 2.288 # Relación PEG histórica, que compara la relación P/E con el crecimiento de las ganancias.

"""