# PFB Yahoo Finance 📈

## Descripción
**PFB Yahoo Finance** es un proyecto que permite extraer y analizar datos financieros de las 100 empresas del **Nasdaq 100**.  
El flujo de trabajo incluye la extracción de datos, procesamiento, análisis y visualización a través de **Streamlit** y **Power BI**.

## Instalación y ejecución 🚀

1. Clonar el repositorio y acceder al directorio del proyecto.  
2. Configurar MySQL modificando la contraseña en el código para que coincida con la configuración local.  
3. Ejecutar el script `obtencion_data_bbdd.py` para extraer y almacenar los datos en la base de datos.  
4. Ejecutar `app_sprint2.py` en Streamlit para visualizar los datos.

## Estructura del proyecto 📂

- **Scraping**: Obtiene la lista de empresas que forman el **Nasdaq 100**.  
- **Extracción de datos**: Descarga información de precios históricos y datos informativos de cada empresa.  
- **Procesamiento**: Limpieza y transformación de los datos antes de subirlos a la base de datos.  
- **Análisis**: Se realiza **clustering** sobre los datos obtenidos.  
- **Visualización**: Uso de **Streamlit** para explorar los datos y un informe en **Power BI** para análisis más profundos.  

## Tecnologías utilizadas 🛠️

- **Python**  
- **Streamlit**  
- **BeautifulSoup / Selenium** (para scraping)  
- **Yahoo Finance API**  
- **MySQL** (base de datos)  
- **Pandas / NumPy** (procesamiento de datos)  
- **Scikit-learn** (clustering)  
- **Power BI** (visualización avanzada)  

## Autores ✨

Este proyecto fue desarrollado por:

- Guadalupe Peña  
- Elsa Melara  
- Marina Domínguez  
- Mikel Alonso  

