import pandas as pd
import numpy as np

#df_historic
#df_historic.info()
#df_historic.describe()
#df_historic.isna().sum()

#pd.set_option("display.max_columns", None)
#df_info
#df_info.info()
#df_info.describe()
#df_info.isna().sum()

def clean_data(df):
    df = df.round(2)
    df = df.replace({np.nan:None})

    return df




