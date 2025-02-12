import streamlit as st
from PIL import Image
from modules.pfb_page_config_dict import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG) 

def main(): 
    st.title("PFB Yahoo Finance")
    st.write("Bienvenidos a la demo del PFB de Yahoo Finance")
    st.sidebar.success("Fases del PFB")

if __name__ == "__main__":  
    main()
