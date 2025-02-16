import mysql.connector

def create_database(database, host = "localhost", user = "root", password = "H3m3t3r10!", use_pure = True):
    db = mysql.connector.connect(host     = host,
                                 user     = user,
                                 password = password,
                                 use_pure = use_pure)
    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
    cursor.close()
    db.close()

def execute_query(query, database, host = "localhost", user = "root", password = "tu_contraseña", use_pure = True):
    db = mysql.connector.connect(host     = host,
                                 user     = user,
                                 password = password,
                                 database = database,
                                 use_pure = use_pure)
    cursor = db.cursor()
    cursor.execute(query)
    cursor.fetchall() # Vaciamos el cursor
    cursor.close()
    db.close()

# Llamada a la función para crear la base de datos
create_database(database = "Yahoo_finance")

# Definimos las queries para crear las tablas
create_historic_table = """
CREATE TABLE IF NOT EXISTS historic (
    Date DATE NOT NULL,
    Ticker VARCHAR(8) NOT NULL,
    Close FLOAT NOT NULL,
    High FLOAT NOT NULL,
    Low FLOAT NOT NULL,
    Open FLOAT NOT NULL,
    Volume BIGINT NOT NULL,
    PRIMARY KEY (Date, Ticker)
);
"""

create_company_info_table = """
CREATE TABLE IF NOT EXISTS company_info (
    Ticker VARCHAR(8) PRIMARY KEY,
    ShortName VARCHAR(255) NOT NULL,
    Sector VARCHAR(255) NOT NULL,
    Industry VARCHAR(255) NOT NULL,
    Country VARCHAR(255) NOT NULL,
    FullTimeEmployees INT,
    MarketCap BIGINT,
    TotalRevenue BIGINT,
    NetIncomeToCommon BIGINT,
    TrailingEPS FLOAT,
    ForwardEPS FLOAT,
    TrailingPE FLOAT,
    ForwardPE FLOAT,
    ReturnOnAssets FLOAT,
    ReturnOnEquity FLOAT,
    DebtToEquity FLOAT,
    FreeCashflow BIGINT,
    DividendRate FLOAT,
    DividendYield FLOAT,
    PayoutRatio FLOAT,
    Beta FLOAT,
    GrossMargins FLOAT,
    OperatingMargins FLOAT,
    ProfitMargins FLOAT,
    ebitdaMargins FLOAT,
    Timestamp_extraction TIMESTAMP
);
"""

# Crear las tablas en la base de datos
execute_query(query = create_historic_table, database = "Yahoo_finance")
execute_query(query = create_company_info_table, database = "Yahoo_finance")
