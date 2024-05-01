import requests
import pandas as pd
from datetime import datetime
from io import BytesIO

class NSE():
    def __init__(self, timeout=10):
        self.base_url = 'https://www.nseindia.com'
        self.session = requests.sessions.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "en-US,en;q=0.9"
        }
        self.timeout = timeout
        self.session.get(self.base_url, timeout=timeout)
        #self.cookies = []
    '''
    def __getCookies(self, renew=False):
        if len(self.cookies) > 0 and renew == False:
            return self.cookies
        r = requests.get(self.base_url, timeout=self.timeout, headers=self.headers)
        self.cookies = dict(r.cookies)
        return self.__getCookies()
    '''
    def getHistoricalData(self, symbol, series, from_date, to_date):
        try:
            url = "/api/historical/cm/equity?symbol={0}&series=[%22{1}%22]&from={2}&to={3}&csv=true".format(symbol.replace('&', '%26'), series, from_date.strftime('%d-%m-%Y'), to_date.strftime('%d-%m-%Y'))
            r = self.session.get(self.base_url + url, timeout=self.timeout)
            df = pd.read_csv(BytesIO(r.content), sep=',', thousands=',')
            df = df.rename(columns={'Date ': 'date', 'series ': 'series', 'OPEN ': 'open', 'HIGH ': 'high', 'LOW ': 'low', 'PREV. CLOSE ': 'prev_close', 'ltp ': 'ltp', 'close ': 'close', '52W H ': 'hi_52_wk', '52W L ': 'lo_52_wk', 'VOLUME ': 'trdqty', 'VALUE ': 'trdval', 'No of trades ': 'trades'})
            df.date = pd.to_datetime(df.date).dt.strftime('%Y-%m-%d')
            return df
        except:
            return None

    def fetch_index_from_nse(self, index_symbol):
        df = []
        res = self.session.get(self.base_url + '/api/equity-stockIndices?index=' + index_symbol, timeout=10)
        if res.status_code == 200:
            res_json = res.json()
            if 'data' in res_json:
                df = pd.json_normalize(res_json['data'])
            else:
                print('Data not returned from NSE')
                print(res_json)
        else:
            print('HTTP Request Failed: ')
            print(res)
        
        return df

    def save_index_to_csv(self, index_symbol, csv_file_name=None, delimiter=',', index=True, header=True):
        if csv_file_name == None:
            csv_file_name = index_symbol + '.csv'

        df = self.fetch_index_from_nse(index_symbol)
        if len(df) > 0:
            df.to_csv(csv_file_name, sep=delimiter, index=index, header=header)
            return True
        
        return False
    
    def getHistoricalRawData(self, symbol, series, from_date, to_date):
        try:
            url = "/api/historical/cm/equity?symbol={0}&series=[%22{1}%22]&from={2}&to={3}&csv=true".format(symbol.replace('&', '%26'), series, from_date.strftime('%d-%m-%Y'), to_date.strftime('%d-%m-%Y'))
            r = self.session.get(self.base_url + url, timeout=self.timeout)
            df = pd.read_csv(BytesIO(r.content), sep=',', thousands=',')
            df = df.rename(columns={'Date ': 'date', 'series ': 'series', 'OPEN ': 'open', 'HIGH ': 'HIGH', 'LOW ': 'LOW', 'PREV. CLOSE ': 'prev_close', 'ltp ': 'ltp', 'close ': 'close', '52W H ': 'hi_52_wk', '52W L ': 'lo_52_wk', 'VOLUME ': 'trdqty', 'VALUE ': 'trdval', 'No of trades ': 'trades'})
            df.date = pd.to_datetime(df.date).dt.strftime('%Y-%m-%d')
            return df
        except:
            return None

if __name__ == '__main__':
    from datetime import date
    from plotly import graph_objs as go
    import mplfinance as mpf
    import matplotlib.pyplot as plt
    import json
    import datetime
    import streamlit as st
    import numpy as np
    import plotly.io as pio
    from plotly.subplots import make_subplots
    from streamlit_option_menu import option_menu
    import os
    import subprocess
    import streamlit.components.v1 as components   
    import yfinance as yf
    import nselib 
    from nselib import capital_market
    import mplfinance as mpf
    import matplotlib.pyplot as plt
    #from datetime import date, datetime
    from pandas_datareader import data as pdr


    nse = NSE()
    selected = option_menu(
                menu_title=None,
                options=["Home","Stock Analysis", "Stock Prediction", "Contact"],
                icons=["house", "rocket","star","envelope"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles={ "container":"width: 150px;"}
            )
    if(selected == 'Home'):
        st.markdown("<h1 style='text-align: center; color: #34568B;'>Stock Market Analyzer and Predictor</h1>", unsafe_allow_html=True)
        with open('C:\\Users\Rao_K\\source\\StockInsights\\apps\\homeContent.txt') as f:
            read_data = f.read()
            st.write("📈" + read_data +"🚀")        
        f.close()
    if(selected == 'Stock Analysis'):
        ind =capital_market.market_watch_all_indices()
        nseIndexes = ind['index']
        indices = st.sidebar.selectbox('Select Index', nseIndexes)        
        stockSymbols = nse.fetch_index_from_nse(indices)
        stocks = stockSymbols['symbol']
        #st.title('🏂 Stock Market Analyzer and Predictor')       
        selected_stock = st.sidebar.selectbox('Select Company', stocks)
        st.markdown(f"""<marquee class="marq" bgcolor="Green", style="color:yellow"; direction="left" loop="">{selected_stock} </marquee>""",unsafe_allow_html=True)

        st.markdown(f"""<h1 style='text-align: center; color: #34568B;'>Real-time Historical data {selected_stock} </h1>""", unsafe_allow_html=True)

        st.sidebar.write("Select Date Range:")
        start_date = st.sidebar.date_input("Enter Start Date:",value=datetime.date(2024,2,1))
        end_date = st.sidebar.date_input("Enter End Date:", value=datetime.date(2024,4,10))
    
        data = nse.getHistoricalData(selected_stock, 'EQ', date(start_date.year,start_date.month,start_date.day), date(end_date.year, end_date.month,end_date.day))
        #print(df)
        #print(nse.fetch_index_from_nse('NIFTY MIDCAP 50'))
        #print(nse.fetch_index_from_nse('NIFTY 50'))

    
        st.write(data)
            #col1, col2 = st.columns(2)
        
            # Plot raw data
        #Time series with range
        def plot_raw_data():
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=data['date'], y=data['open'], name="stock_open"))
                    fig.add_trace(go.Scatter(x=data['date'], y=data['close'], name="stock_close"))
                    fig.layout.update(title_text='Time Series with Range : ' + selected_stock, xaxis_rangeslider_visible=True)
                    st.plotly_chart(fig)   

        plot_raw_data()

        # Plot moving average
        df = pd.DataFrame(data)
        df['MA5'] = df.close.rolling(5).mean()
        df['MA20'] = df.close.rolling(20).mean()
        # plot the candlesticks
        fig = go.Figure(data=[go.Candlestick(x=df.date,
                                            open=df.open, 
                                            high=df.high,
                                            low=df.low,
                                            close=df.close), 
                            go.Scatter(x=df.date, y=df.MA5, line=dict(color='orange', width=1)),
                            go.Scatter(x=df.date, y=df.MA20, line=dict(color='green', width=1))])
        fig.layout.update(title_text='Moving Average : ' + selected_stock)
        st.write(fig)

        #Candle stick
        fig1 = go.Figure(data=[go.Candlestick(x=data['date'],
                                open=data['open'],
                                high=data['high'],
                                low=data['low'],
                                increasing_line_color= 'cyan', decreasing_line_color= 'gray',
                                close=data['close'])])
        fig1.layout.update(title_text='Candle stick : ' + selected_stock, xaxis_rangeslider_visible=True)
        st.write(fig1)

        #RSI (Relative Strength Index)
        def RSI(series, period):
            delta = series.diff().dropna()
            u = delta * 0
            d = u.copy()
            u[delta > 0] = delta[delta > 0]
            d[delta < 0] = -delta[delta < 0]
            u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
            u = u.drop(u.index[:(period-1)])
            d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
            d = d.drop(d.index[:(period-1)])
            rs = pd.DataFrame.ewm(u, com=period-1, adjust=False).mean() / \
                pd.DataFrame.ewm(d, com=period-1, adjust=False).mean()
            return 100 - 100 / (1 + rs)

        df['RSI'] = RSI(df.close,14)
        dff = df.tail(180)
        layoutt = go.Layout(autosize=False, width=4181, height=1597)
        # make it fit on my screen!!!
        layoutt = go.Layout(autosize=True)
        layoutt2 = go.Layout(autosize=False, width=6731, height=2571)
        fig2 = go.Figure(
            data=[
                go.Candlestick(
                    x=dff["date"],
                    open=dff["open"],
                    high=dff["high"],
                    low=dff["low"],
                    close=dff["close"],
                    name="OHLC",
                ),
                go.Scatter(
                    x=dff["date"], y=dff["RSI"], mode="markers+lines", name="RSI", yaxis="y2"
                ),
            ],
            layout=layoutt,
        ).update_layout(
            yaxis_domain=[0.3, 1],
            yaxis2={"domain": [0, 0.20]},
            xaxis_rangeslider_visible=False,
            showlegend=False    
        )
        fig2.layout.update(title_text='RSI Indicator : ' + selected_stock, xaxis_rangeslider_visible=True)

        st.write(fig2)

        #Moving average convergence/divergence (MACD) is a trend-following momentum indicator that shows the relationship between two exponential moving averages (EMAs) of a security's price.

        pio.templates.default = "plotly_white"

        fig3 = make_subplots(vertical_spacing = 0, rows=3, cols=1, row_heights=[0.6, 0.2, 0.2])

        fig3.add_trace(go.Candlestick(x=df['date'],
                                    open=df['open'],
                                    high=df['high'],
                                    low=df['low'],
                                    close=df['close']))

        fig3.add_trace(go.Scatter(x=df['date'], y = df['MA5']), row=2, col=1)
        fig3.add_trace(go.Scatter(x=df['date'], y = df['MA5']*1.1), row=2, col=1)
        fig3.add_trace(go.Bar(x=df['date'], y = df['trdqty']), row=3, col=1)

        fig3.update_layout(xaxis_rangeslider_visible=False,
                        xaxis=dict(zerolinecolor='black', showticklabels=False),
                        xaxis2=dict(showticklabels=False))

        fig3.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=False)
        fig3.layout.update(title_text='MACD Indicator : ' + selected_stock, xaxis_rangeslider_visible=True)

        st.write(fig3)
    if(selected == 'Stock Prediction'):
        st.write('Predict the Stock')
        #stocks = yf.Tickers()
        ind =capital_market.market_watch_all_indices()
        nseIndexes = ind['index']
        indices = st.sidebar.selectbox('Select Index', nseIndexes)        
        stockSymbols = nse.fetch_index_from_nse(indices)
        stocks = stockSymbols['symbol']
        #st.title('🏂 Stock Market Analyzer and Predictor')       
        selected_stock = st.sidebar.selectbox('Select Company', stocks)
        st.markdown(f"""<marquee class="marq" bgcolor="Green" direction="left" loop="">{selected_stock} </marquee>""",unsafe_allow_html=True)

        st.markdown(f"""<h1 style='text-align: center; color: #34568B;'>Real-time Historical data {selected_stock} </h1>""", unsafe_allow_html=True)

        st.sidebar.write("Select Date Range:")
        start_date = st.sidebar.date_input("Enter Start Date:",value=datetime.date(2024,2,1))
        end_date = st.sidebar.date_input("Enter End Date:", value=datetime.date(2024,4,10))
    
        #data = nse.getHistoricalData(selected_stock, 'EQ', date(start_date.year,start_date.month,start_date.day), date(end_date.year, end_date.month,end_date.day))
        #print(df)
        #print(nse.fetch_index_from_nse('NIFTY MIDCAP 50'))
        #print(nse.fetch_index_from_nse('NIFTY 50'))

    
        #st.write(data)
        companyName=selected_stock + '.NS';
        st.write(companyName)
        stock = yf.Ticker(companyName)
        #st.write(stock.info)
        # get historical market data
        hist = stock.history(period="12mo")
        st.markdown('&nbsp;')
        show_data = st.checkbox('Show data table', False)
        if show_data:  
            st.write(hist)
        #fig4 = mpf.plot(hist, type='candle', title= selected_stock+" Candlestick Chart (Daily)", style='yahoo', figscale = 2.0, figratio = (1, 0.3),returnfig=True)
        #st.plt(fig4)
        mav1 = st.number_input('Mav 1', min_value=3, max_value=30, value=3, step=1)
        mav2 = st.number_input('Mav 2', min_value=3, max_value=30, value=6, step=1)
        mav3 = st.number_input('Mav 3', min_value=3, max_value=30, value=9, step=1)        
        fig5, ax = mpf.plot(
            hist,
            title=selected_stock +" Candlestick Chart (Daily)",
            type='candle',
            mav=(int(mav1),int(mav2),int(mav3)),
            volume=True,

            style='yahoo',
            figsize=(15,10),
            returnfig=True
            )

        st.pyplot(fig5)
    
    if(selected == 'Contact'):
        st.write("Email:-kurmaraopalli@yahoo.com")
        st.write("Thanks for contacting...!")
        st.cache_data(persist='disk')
        def get_historical_data(symbol, start_date = None):
            df = pdr.get_data_yahoo(symbol, start=start_date, end=datetime.now())
            df = df.rename(columns = {'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj close', 'Volume': 'volume'})
            for i in df.columns:
                df[i] = df[i].astype(float)
            df.index = pd.to_datetime(df.index)
            if start_date:
                df = df[df.index >= start_date]
            return df

        st.title('mplfinance demo')

        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            symbol = st.selectbox('Choose stock symbol', options=['AAPL', 'MSFT', 'GOOG', 'AMZN'], index=1)
        with c2:
            date_from = st.date_input('Show data from', date(2023, 10, 1))
        with c3:
            st.markdown('&nbsp;')
            show_data = st.checkbox('Show data table', False)

        st.markdown('---')

        st.sidebar.subheader('Settings')
        st.sidebar.caption('Adjust charts settings and then press apply')

        with st.sidebar.form('settings_form'):
            show_nontrading_days = st.checkbox('Show non-trading days', True)
            # https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
            chart_styles = [
                'default', 'binance', 'blueskies', 'brasil', 
                'charles', 'checkers', 'classic', 'yahoo',
                'mike', 'nightclouds', 'sas', 'starsandstripes'
            ]
            chart_style = st.selectbox('Chart style', options=chart_styles, index=chart_styles.index('starsandstripes'))
            chart_types = [
                'candle', 'ohlc', 'line', 'renko', 'pnf'
            ]
            chart_type = st.selectbox('Chart type', options=chart_types, index=chart_types.index('candle'))

            mav1 = st.number_input('Mav 1', min_value=3, max_value=30, value=3, step=1)
            mav2 = st.number_input('Mav 2', min_value=3, max_value=30, value=6, step=1)
            mav3 = st.number_input('Mav 3', min_value=3, max_value=30, value=9, step=1)

            st.form_submit_button('Apply')

        data = get_historical_data(symbol, str(date_from))

        fig, ax = mpf.plot(
            data,
            title=f'{symbol}, {date_from}',
            type=chart_type,
            show_nontrading=show_nontrading_days,
            mav=(int(mav1),int(mav2),int(mav3)),
            volume=True,

            style=chart_style,
            figsize=(15,10),
            
            # Need this setting for Streamlit, see source code (line 778) here:
            # https://github.com/matplotlib/mplfinance/blob/master/src/mplfinance/plotting.py
            returnfig=True
        )

        st.pyplot(fig)

        if show_data:
            st.markdown('---')
            st.dataframe(data)
    
       