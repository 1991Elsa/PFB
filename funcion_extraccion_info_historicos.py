from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer, Float, DateTime, Date
import pandas as pd
from create_engine import create_engine

password = create_engine()



# Crear el engine de conexión sin especificar una base de datos
try:
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/')
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexión establecida con éxito y librerías instaladas correctamente.")
    
    # Conectarse y crear la base de datos 'yahoo_finance'
    with engine.connect() as connection:
        connection.execute(text("CREATE DATABASE IF NOT EXISTS yahoo_finance"))
        print("Base de datos yahoo_finance creada con éxito.")
    
    # Ahora conectar al motor especificando la nueva base de datos
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/yahoo_finance')
    # Verificar la conexión a la nueva base de datos
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexión establecida con éxito a la base de datos yahoo_finance y librerías instaladas correctamente.")
except Exception as e:
    print(f"Error al establecer la conexión: {e}")

# Crear el objeto MetaData
metadata = MetaData()

# Definir la tabla nasdaq_tickers_info_sql con Ticker como clave primaria y Timestamp_extraction como DATETIME
tickers_info_table = Table('nasdaq_tickers_info_sql', metadata,
    Column('Ticker', String(10), primary_key=True, unique=True),
    Column('ShortName', String(100)),
    Column('Sector', String(50)),
    Column('Industry', String(50)),
    Column('Country', String(50)),
    Column('FullTimeEmployees', Float),
    Column('MarketCap', Integer),
    Column('TotalRevenue', Integer),
    Column('NetIncomeToCommon', Integer),
    Column('TrailingEPS', Float),
    Column('ForwardEPS', Float),
    Column('TrailingPE', Float),
    Column('ForwardPE', Float),
    Column('ReturnOnAssets', Float),
    Column('ReturnOnEquity', Float),
    Column('DebtToEquity', Float),
    Column('FreeCashflow', Float),
    Column('DividendRate', Float),
    Column('DividendYield', Float),
    Column('PayoutRatio', Float),
    Column('Beta', Float),
    Column('GrossMargins', Float),
    Column('OperatingMargins', Float),
    Column('ProfitMargins', Float),
    Column('ebitdaMargins', Float),
    Column('Timestamp_extraction', DateTime)  # Tipo DATETIME
)

# Crear la tabla nasdaq_tickers_info_sql en la base de datos
try:
    tickers_info_table.create(engine)
    print("Tabla nasdaq_tickers_info_sql creada con éxito.")
except Exception as e:
    print(f"Error al crear la tabla nasdaq_tickers_info_sql: {e}")

# Definir la tabla nasdaq_tickers_historic_sql con Date como DATE
tickers_historic_table = Table('nasdaq_tickers_historic_sql', metadata,
    Column('Date', Date),
    Column('Ticker', String(10)),
    Column('Close', Float),
    Column('High', Float),
    Column('Low', Float),
    Column('Open', Float),
    Column('Volume', Float)
)

# Crear la tabla nasdaq_tickers_historic_sql en la base de datos
try:
    tickers_historic_table.create(engine)
    print("Tabla nasdaq_tickers_historic_sql creada con éxito.")
except Exception as e:
    print(f"Error al crear la tabla nasdaq_tickers_historic_sql: {e}")


# Leer los DataFrames desde los archivos CSV
try:
    df_nasdaq_tickers_info_clean = pd.read_csv('nasdaq_tickers_info_clean.csv')
    df_nasdaq_tickers_historic_clean = pd.read_csv('nasdaq_tickers_historic_clean.csv')

    # Asegurarse de que las columnas 'Timestamp_extraction' y 'Date' son del tipo correcto
    df_nasdaq_tickers_info_clean['Timestamp_extraction'] = pd.to_datetime(df_nasdaq_tickers_info_clean['Timestamp_extraction'])
    df_nasdaq_tickers_historic_clean['Date'] = pd.to_datetime(df_nasdaq_tickers_historic_clean['Date']).dt.date

    # Insertar los datos en la tabla nasdaq_tickers_info_sql
    try:
        df_nasdaq_tickers_info_clean.to_sql(name='nasdaq_tickers_info_sql', con=engine, if_exists='replace', index=False)
        print("Datos insertados en la tabla nasdaq_tickers_info_sql correctamente.")
    except Exception as e:
        print(f"Error al insertar los datos en la tabla nasdaq_tickers_info_sql: {e}")

    # Insertar los datos en la tabla nasdaq_tickers_historic_sql
    try:
        df_nasdaq_tickers_historic_clean.to_sql(name='nasdaq_tickers_historic_sql', con=engine, if_exists='replace', index=False)
        print("Datos insertados en la tabla nasdaq_tickers_historic_sql correctamente.")
    except Exception as e:
        print(f"Error al insertar los datos en la tabla nasdaq_tickers_historic_sql: {e}")

except Exception as e:
    print(f"Error al leer los archivos CSV o insertar los datos en las tablas: {e}")