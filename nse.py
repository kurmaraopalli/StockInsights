#pip install yfinance pandas mplfinance TA-Lib        
import yfinance as yf
import streamlit as st
from nsetools import Nse
#import mplfinance as mpf
#import matplotlib.pyplot as plt
from plotly import graph_objs as go

st.title("NSE")
stock = yf.Ticker("TATASTEEL.NS")
#print(stock.info)
# get historical market data
hist = stock.history(period="12mo")     
st.write(hist.tail())

nse = Nse()
inq = nse.get_quote('infy')
st.write(inq.tail())
#mpf.plot(hist, type='candle', title="TATASTEEL Candlestick Chart (Daily)", style='yahoo', figscale = 2.0, figratio = (1, 0.3))        
