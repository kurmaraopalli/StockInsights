import streamlit as st
#from streamlit_navigation_bar import st_navbar
import os
import subprocess
import sys
#from streamlit_option_menu import option_menu
from multiapp import MultiApp
from apps import home, data, model, about # import your app modules here

app = MultiApp()
#with st.sidebar:
'''    selected = option_menu(
            menu_title=None,
            options=["Home","Indian Stocks", "US Stocks", "About"],
            icons=["house", "rocket","star","envelope"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"

        )
#page = st_navbar(["NSE", "BSE", "NASDOC", "S&P", "About"])
    if(selected == "Home"):
        homeContent=open("homepage.txt","r")
        st.write("Stock market analyzer and predictor")
        st.write("📈" + homeContent.read() +"🚀")
        homeContent.close()
    if(selected == "Indian Stocks"):
        app.add_app("Indian Stocks", histnse.app)
    if(selected == "US Stocks"):
        st.write(selected)   
    if(selected == "S&P"):
        st.write(selected)    
    if(selected == "About"):
        st.title =""
        st.write("Create a robust tool that analyzes historical stock data, identifies trends, and provides actionable insights.")             

#app.run()'''
app.add_app("Home", home.app)
app.add_app("about", about.app)
# The main app
app.run()
