from PIL import Image

# Configuración de la página con los parámetros que se desean en formato de diccionario.
PAGE_CONFIG = {"page_title"            : "NDQ 100",     # Título de la página
               "page_icon"             : Image.open("sources/logo_ndq.jpeg"), # Icono de la página
               "layout"                : "wide",     
               "initial_sidebar_state" : "collapsed"} # collapsed o expanded para que el menu este abierto o cerrado por defecto