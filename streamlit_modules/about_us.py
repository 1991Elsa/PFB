import pandas as pd
import numpy as np
import streamlit as st


def mostrar(nasdaq_tickers_historic, nasdaq_tickers_info):
    st.title("📍​ About Us")

    st.write("\n")
    st.write("Aplicación desarrollada por estudiantes de Hackaboss en el bootcamp de Data Analytics.")
    st.write("\n")

    st.header("Tecnologías Utilizadas:")

    st.write("\n")
    st.write("\n")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### Desarrollo")
        st.image("sources/I_Python.png") 
        st.markdown("**Python**")
        
    with col2:
        st.markdown("### Bases de Datos")
        st.image("sources/I_MySQL.png")
        st.markdown("**MySQL Workbench**")
    
    with col3:
        st.markdown("### Desarrollo Web")
        st.image("sources/I_Streamlit.png")
        st.markdown("**Streamlit**")

    with col4:
        st.markdown("### Visualizaciones")
        st.image("sources/I_PowerBI.png")
        st.markdown("**Power BI**")

    st.write("\n")
    st.write("\n")

    st.header("Proceso de Desarrollo:")
        
    st.write("\n")
    st.write("\n")
    st.image("sources/D_F_proyecto.drawio.png")
    st.write("\n")
    st.write("\n")
        
    st.header("Equipo de Desarrollo:")

    st.write("\n")
    st.write("\n")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**Elsa Melara**")
        st.write("[LinkedIn](https://www.linkedin.com/in/elsa-m-356055b9) | [GitHub](https://github.com/1991Elsa)")
        st.image("https://github.com/1991Elsa.png", width=100)
        

    with col2:    
        st.markdown("**Guadalupe Peña**")
        st.write("[LinkedIn](https://www.linkedin.com/in/guadalupe-peña-egea-3aaa8b329) | [GitHub](https://github.com/AdaXana)")
        st.image("https://ca.slack-edge.com/T01LJTV7F8F-U07PHJDQ2UU-1cd26fc26974-72", width=100)

    with col3:
        st.markdown("**Marina Dominguez**")
        st.write("[LinkedIn](https://www.linkedin.com/in/marina-dominguez-28639b325) | [GitHub](https://github.com/Marina90d)")
        st.image("https://ca.slack-edge.com/T01LJTV7F8F-U07PF3P8GSE-aaba0a24d2c9-72", width=100)

    with col4:
        st.markdown("**Mikel Alonso**")
        st.write("[LinkedIn](https://www.linkedin.com/in/mikel-alonso-alvarez-187776328) | [GitHub](https://github.com/Wantumaka)")
        st.image("https://media.licdn.com/dms/image/v2/D4E03AQHI8B3GYBXpTA/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1726060899129?e=1747267200&v=beta&t=r7sEmfM8nP1vcQz0FUBGXRmu2nfc5dTvTP7x5OHGY9g", width=100)



