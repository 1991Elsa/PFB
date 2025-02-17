import pandas as pd
import sklearn

from dotenv import load_dotenv 
import os


# configuración
load_dotenv(dotenv_path=".config_engine")

password = os.getenv("password")
username = os.getenv("username")
host = os.getenv("host")
port  = os.getenv("port")

print(f"password: {password}")
#print(f"username: {username}")
print(f"host: {host}")
print(f"port: {port}")

if None in [password, username, host, port]:
    raise ValueError("Una de las variables de entorno no se ha cargado correctamente")

#assert username == "root", f"Se espera que el username sea root pero se obtiene {username}"

# Crear el engine de conexión sin especificar una base de datos
engine = create_engine(f'mysql+pymysql://{"root"}:{password}@{host}:{port}/')

# Ahora conectar al motor especificando la nueva base de datos
engine = create_engine(f'mysql+pymysql://{"root"}:{password}@{host}:{port}/yahoo_finance')
