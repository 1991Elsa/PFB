import pandas as pd
import numpy as np

nasdaq_tickers_historic = pd.read_csv('nasdaq_tickers_historic_clean.csv')
nasdaq_tickers_info = pd.read_csv('nasdaq_tickers_info_clean.csv')

print(nasdaq_tickers_historic.describe())
print(nasdaq_tickers_info.describe())

