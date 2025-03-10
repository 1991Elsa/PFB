import streamlit as st

def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("Dashboard Power BI")
    st.write("\n")
    powerbi_width = 800
    powerbi_height = 500
    st.markdown(body = f'<iframe title="dashboard PBI" width="{powerbi_width}" height="{powerbi_height}" src="https://app.powerbi.com/view?r=eyJrIjoiN2ZhYTI2ZTAtMDU2Ni00NDc0LWFlMjAtNWY4ZmU4ZmFjMjBmIiwidCI6IjVlNzNkZTM1LWU4MjUtNGVkNS1iZTIyLTg4NTYzNTI3MDkxZSIsImMiOjl9&pageName=3bc6606a3e224c56187f" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)