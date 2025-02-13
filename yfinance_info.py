# yfinance_info.py
"""
Información sobre la librería yfinance.

yfinance es una librería de Python que permite acceder a datos financieros históricos
y en tiempo real de Yahoo Finance.

Instalación:
------------
Puedes instalar yfinance usando pip:
pip install yfinance

Ejemplo de uso:
---------------
Aquí hay un ejemplo básico de cómo usar yfinance para obtener datos históricos de una acción:

import yfinance as yf

# Obtener los datos históricos de Apple (AAPL)
aapl = yf.Ticker("AAPL")
hist = aapl.history(period="1mo")

# Mostrar los datos históricos
print(hist)
"""

# Ejemplo básico de uso
import yfinance as yf

# Obtener los datos históricos de Apple (AAPL)
aapl = yf.Ticker("AAPL")
hist = aapl.history(period="1mo")

# Mostrar los datos históricos
print(hist)
