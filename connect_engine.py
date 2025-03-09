from sqlalchemy import create_engine

DATABASE_CONFIG = {
    "username": "root",
    "password": "Dunidu",
    "hostname": "localhost", 
    "port": 3306
}

def get_engine():
    connection_string = f"mysql+pymysql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['hostname']}:{DATABASE_CONFIG['port']}"
    engine = create_engine(connection_string)
    return engine

def get_engine_database():
    database_name = "yahoo_finance_nasdaq_100"
    connection_string = f"mysql+pymysql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['hostname']}:{DATABASE_CONFIG['port']}/{database_name}"
    engine = create_engine(connection_string)
    return engine