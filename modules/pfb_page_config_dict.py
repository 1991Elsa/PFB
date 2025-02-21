from PIL import Image

# Configuración de la página con los parámetros que se desean en formato de diccionario.
PAGE_CONFIG = {"page_title"            : "PFB Yahoo! Finance",     # Título de la página
               "page_icon"             : Image.open("sources/YF_icono.png"), # Icono de la página
               "layout"                : "wide",     
               "initial_sidebar_state" : "collapsed"} 