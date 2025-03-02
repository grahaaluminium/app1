import streamlit as st
import time
import pandas as pd
import numpy as np
import random
import datetime as dt
import yfinance as yf

# Load dataset ticker
data_stooq_ticker = pd.read_csv('https://raw.githubusercontent.com/guangyoung/dataStock/refs/heads/main/stooq_tickers.csv')
data_yfinance_ticker = pd.read_csv('https://raw.githubusercontent.com/guangyoung/dataStock/refs/heads/main/yfinance_tickers.csv')  # Perbaiki sumber

# Header UI
st.markdown(
    """
    <div style='text-align: center; margin-top: -53px;'>
        <img src='https://e7.pngegg.com/pngimages/589/237/png-clipart-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-thumbnail.png' width='120'>
    </div>
    <p style='text-align: center; margin-top: 10px; font-size: 18px;'>
        Test me using any stock from any data source, any exchange, over any period.
    </p>
    """, unsafe_allow_html=True
)

# Sidebar Menu
def sidebar_menu():
    st.sidebar.markdown(
        """
        <div style='text-align: center; margin-top: -60px;'>
            <img src='https://e7.pngegg.com/pngimages/589/237/png-clipart-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-thumbnail.png' width='150'>
        </div>
        <p style='text-align: center; font-size: 30px;'><b>QUANTGENIUS</b></p>
        <p style='text-align: center; font-size: 20px;'>Artificial Superintelligence Quantitative Trading System</p>
        """, unsafe_allow_html=True
    )

    with st.sidebar.expander("Input your QuantGenius API Key", expanded=False):
        api_key1 = st.text_input("Enter your QuantGenius API Key1", type="password")
        if api_key1:
            st.success("QuantGenius API Key successfully entered!")
        st.markdown(
            "<p style='font-size: 12px'>Don't have QuantGenius API Key? <a href='https://www.kompas.com' target='_blank'>Click here</a></p>",
            unsafe_allow_html=True
        )

    with st.sidebar.expander("Setting your test parameter", expanded=False):
        # Dropdown settings
        st.selectbox('Initial Equity', options=[1000000, 2000000, 3000000, 4000000])        
        st.selectbox('Commission per trade', options=[0.001, 0.002, 0.003])        
        st.selectbox('Spread + Slippage per size', options=[0.001, 0.002, 0.003])        
        st.selectbox('Interest Rate per year', options=[0.02, 0.03, 0.04])        
        st.selectbox('Initial Margin Requirement', options=[0.1, 0.2, 0.3])        
        st.selectbox('Margin Maintenance', options=[0.1, 0.2, 0.3])

sidebar_menu()

# Pilihan Data Source
dropdown_dataSource = st.selectbox('Select Data Source', options=['Yahoo Finance', 'Stooq', 'Tiingo', 'Alphavantage', 'Montecarlo Simulation', 'Local Data'], key="target_lang")  

if dropdown_dataSource == 'Local Data':
    uploaded_files = st.file_uploader("Choose 30 stock file for your portfolio", type=["txt", "csv"], accept_multiple_files=True)

    if uploaded_files:
        uploaded_filenames = set()
        for uploaded_file in uploaded_files:
            if uploaded_file.name in uploaded_filenames:
                st.error(f"File '{uploaded_file.name}' sudah ada! Harap buang duplikatnya.")
            else:
                uploaded_filenames.add(uploaded_file.name)
        if len(uploaded_files) < 4:
            st.warning(f"Total file yang dipilih kurang {4-len(uploaded_files)} file.")
        else:
            st.success("Proses selesai!")

elif dropdown_dataSource == 'Yahoo Finance':
    dropdown_yahooExchange = st.selectbox('Select Exchange', options=['nasdaq', 'nyse', 'nysemkt'])

    # Dropdown untuk memilih tahun mulai
    start_year = st.selectbox("Start Year:", options=[str(year) for year in range(1991, 2015)], index=0)
    
    ticker_data = data_yfinance_ticker
    if dropdown_yahooExchange in ticker_data.columns:
        options = [
            stock for stock in ticker_data[dropdown_yahooExchange].dropna().tolist()
            if dt.datetime.strptime(stock.split(',')[1], '%Y%m%d').year < int(start_year)
        ]
    else:
        options = []

    if dropdown_yahooExchange == 'nasdaq':
        yahoo_ticker = st.multiselect('Select 30 Stocks or click "Choose Random Stocks" above', options, default=[])

test_button = st.button("Connect to QuantGenius AI engine for real-time trade signals")

if test_button:
    if 'yahoo_ticker' in locals() and len(yahoo_ticker) == 30:
        portfolio_data, portfolio_ticker = [], []

        for ticker in yahoo_ticker:
            ticker_symbol = ticker.split('.')[0]
            ticker_data = yf.download(ticker_symbol, period="max")
            if len(ticker_data) > 100 and ticker_symbol not in portfolio_ticker:
                portfolio_data.append(ticker_data['Close'])
                portfolio_ticker.append(ticker_symbol)
                st.write(ticker_data)
        
        if len(portfolio_data) >= 5:
            test_start_date = max(data.index.min() for data in portfolio_data)
            test_end_date = min(data.index.max() for data in portfolio_data)
            date_range = pd.date_range(test_start_date, test_end_date).to_list()
            test_data = pd.DataFrame(
                [[data.loc[date] if date in data.index else data.iloc[-1] for data in portfolio_data] for date in date_range],
                index=date_range
            )
            st.write(test_data)

    else:
        st.error("Portfolio data belum ada atau belum dibuat!")

st.markdown("<p style='text-align: left; font-size: 12px;'><i>- Learn more about this testing... <a href='https://www.kompas.com'>Learn more</a></i></p>", unsafe_allow_html=True)
