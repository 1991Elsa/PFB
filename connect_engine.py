from sqlalchemy import create_engine

DATABASE_CONFIG = {
    "username": "root",
<<<<<<< HEAD
    "password": "2021",
=======
    "password": "H3m3t3r10!",
>>>>>>> 55df5eb3ca054277240c952a9ab3be0e1d422be0
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