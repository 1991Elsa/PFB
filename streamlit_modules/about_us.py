import pandas as pd
import numpy as np
import streamlit as st


def mostrar():
    st.title("About Us")

    st.write("\n")
    st.write("Aplicación desarrollada por estudiantes de Hackaboss en el bootcamp de Data Analytics.")
    st.write("\n")

    st.header("Tecnologías Utilizadas:")

    st.write("\n")
    st.write("\n")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("### **Python**")
        st.write("Pandas") 
        st.write("Numpy") 
        st.write("Plotly") 
        st.write("Scikit-learn")

    with col2:
        st.markdown("### **Bases de Datos**")
        st.write("**MySQL Workbench**")
    
    with col3:
        st.markdown("### **Desarrollo Web**")    
        st.write("**Streamlit**")

    with col4:
        st.markdown("### **Visualizaciones**")
        st.write("**Power BI**")

    st.write("\n")
    st.write("\n")

    st.header("Proceso de Desarrollo:")
        
    st.write("\n")
    st.write("\n")
    st.write("1. Extracción y tratamiento de datos:")
    st.write("2. Creación de base de datos:")
    st.write("3. Modelado de datos MySQL.")
    st.write("4. Análisis de datos y visualización.")
    st.write("5. Desarrollo de Modelos de Machine Learning - Clustering y Clasificación.")
    st.write("6. Creación de aplicación interactiva.")
    st.write("7. Integración de Power BI para vista usuario.")
    
    st.write("\n")
    st.write("\n")
        
    st.header("Equipo de Desarrollo:")

    st.write("\n")
    st.write("\n")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**Elsa Melara**")
        st.write("[LindedIn](https://www.linkedin.com/in/elsa-m-356055b9) | [GitHub](https://github.com/1991Elsa)")
        st.image("https://github.com/1991Elsa.png", width=100)
        

    with col2:    
        st.markdown("**Guadalupe Peña**")
        st.write("[LindedIn](https://www.linkedin.com/in/guadalupe-peña-egea-3aaa8b329) | [GitHub](https://github.com/AdaXana)")
        st.image("https://github.com/AdaXana.png", width=100)

    with col3:
        st.markdown("**Marina Dominguez**")
        st.write("[LindedIn](https://www.linkedin.com/in/marina-dominguez-28639b325) | [GitHub](https://github.com/Marina90d)")
        st.image("https://github.com/Marina90d.png", width=100)

    with col4:
        st.markdown("**Mikel Alonso**")
        st.write("[LindedIn](https://www.linkedin.com/in/mikel-alonso-alvarez-187776328) | [GitHub](https://github.com/Wantumaka)")
        st.image("https://github.com/Wantumaka.png", width=100)



