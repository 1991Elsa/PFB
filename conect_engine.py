from sqlalchemy import create_engine

def get_engine():
    username = 'root'
    password = 'H3m3t3r10!'
    host = 'localhost'
    port = '3306'
    
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/')
    return engine

def get_engine_database():
    username = 'root'
    password = 'H3m3t3r10!'
    host = 'localhost'
    port = '3306'
    database = 'yahoo_finance'
    
    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')
    return engine
