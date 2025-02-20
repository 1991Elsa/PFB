#tablas_metadata.py

from sqlalchemy import MetaData, Table, Column, String, Float, DateTime, Date, ForeignKey, text, insert

metadata = MetaData()

tickers_info_table = Table('nasdaq_tickers_info_sql', metadata,
    Column('Ticker', String(10), primary_key=True),
    Column('ShortName', String(100)),
    Column('Sector', String(50)),
    Column('Industry', String(50)),
    Column('Country', String(50)),
    Column('MarketCap', Float),
    Column('TotalRevenue', Float),
    Column('NetIncomeToCommon', Float),
    Column('ReturnOnAssets', Float),
    Column('ReturnOnEquity', Float),
    Column('DebtToEquity', Float),
    Column('FreeCashflow', Float),
    Column('DividendRate', Float),
    Column('DividendYield', Float),
    Column('PayoutRatio', Float),
    Column('GrossMargins', Float),
    Column('OperatingMargins', Float),
    Column('ProfitMargins', Float),
    Column('ebitdaMargins', Float),
    Column('Timestamp_extraction', DateTime) 
)

tickers_historic_table = Table('nasdaq_tickers_historic_sql', metadata,
    Column('Date', Date, primary_key=True),
    Column('Ticker', String(10), ForeignKey('nasdaq_tickers_info_sql.Ticker'), primary_key=True),  
    Column('Close', Float),
    Column('High', Float),
    Column('Low', Float),
    Column('Open', Float),
    Column('Volume', Float)
)

