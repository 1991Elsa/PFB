import pandas as pd
import numpy as np

df_info = pd.read_csv("nasdaq_info")
df_historic = pd.read_csv("nasdaq_historic")


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


df_historic = clean_data(df_historic)
df_info = clean_data(df_info)

df_info.to_csv("data_info", index=False)
df_historic.to_csv("data_historic", index=False)



