import streamlit as st
from streamlit_navigation_bar import st_navbar
import os


page = st_navbar(["NSE", "BSE", "NASDOC", "S&P", "About"])
if(page == "NSE"):
    os.system(r'python C:\Users\Rao_K\source\StockInsights\histnse.py')
    #os.system("python histnse.py")
    # file_2.py
    #with open("C:\Users\Rao_K\source\StockInsights\histnse.py") as file:
     #   exec(file.read())
if(page == "BSE"):
    st.write(page)
if(page == "NASDOC"):
    st.write(page)   
if(page == "S&P"):
    st.write(page)    
if(page == "About"):
    st.title =""
    st.write("Create a robust tool that analyzes historical stock data, identifies trends, and provides actionable insights.")             


