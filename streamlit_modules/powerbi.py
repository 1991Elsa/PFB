import streamlit as st

def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("Dashboard Power BI")
    import streamlit as st

    

    # URL del informe embebido (reemplázala si tienes el enlace de compartir)
    power_bi_url = "https://app.powerbi.com/view?r=12771cb3-7c0d-42f9-89df-5f8ac84a9104"

    # Insertar el iframe en Streamlit
    st.components.v1.iframe(power_bi_url, width=900, height=800)
