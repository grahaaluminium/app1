import streamlit as st
import pandas as pd
import numpy as np
import random
import datetime as dt
import yfinance as yf

# Load ticker data
url_stooq = 'https://raw.githubusercontent.com/guangyoung/dataStock/main/stooq_tickers.csv'
url_yfinance = 'https://raw.githubusercontent.com/guangyoung/dataStock/main/yfinance_tickers.csv'

try:
    data_stooq_ticker = pd.read_csv(url_stooq)
    data_yfinance_ticker = pd.read_csv(url_yfinance)
except Exception as e:
    st.error(f"Error loading ticker data: {e}")

# UI Setup
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://e7.pngegg.com/pngimages/589/237/png-clipart-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-thumbnail.png' width='120'>
    </div>
    <p style='text-align: center; font-size: 18px;'>
        Test me using any stock from any data source, any exchange, over any period.
    </p>
""", unsafe_allow_html=True)

# Sidebar
def sidebar_menu():
    st.sidebar.markdown("""
        <div style='text-align: center;'>
            <img src='https://e7.pngegg.com/pngimages/589/237/png-clipart-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-thumbnail.png' width='150'>
        </div>
        <p style='text-align: center; font-size: 30px'><b>QUANTGENIUS</b></p>
        <p style='text-align: center; font-size: 20px'>Artificial Superintelligence Quantitative Trading System</p>
    """, unsafe_allow_html=True)
    
    with st.sidebar.expander("Input your QuantGenius API Key", expanded=False):
        api_key1 = st.text_input("Enter your QuantGenius API Key", type="password")
        if api_key1:
            st.success("API Key entered successfully!")
    
    with st.sidebar.expander("Setting your test parameter", expanded=False):
        st.selectbox('Initial Equity', options=[1000000, 2000000, 3000000, 4000000])
        st.selectbox('Commission per trade', options=[0.001, 0.002, 0.003])
        st.selectbox('Spread + Slippage per size', options=[0.001, 0.002, 0.003])
        st.selectbox('Interest Rate per year', options=[0.02, 0.03, 0.04])
        st.selectbox('Initial Margin Requirement', options=[0.1, 0.2, 0.3])
        st.selectbox('Margin Maintenance', options=[0.1, 0.2, 0.3])

sidebar_menu()

# Data Source Selection
dropdown_dataSource = st.selectbox(
    'Select Data Source',
    options=['Yahoo Finance', 'Stooq', 'Tiingo', 'Alphavantage', 'Montecarlo Simulation', 'Local Data']
)

# Handle Local Data Upload
if dropdown_dataSource == 'Local Data':
    uploaded_files = st.file_uploader("Upload stock data files", type=["txt", "csv"], accept_multiple_files=True)
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} files")

# Handle Yahoo Finance
elif dropdown_dataSource == 'Yahoo Finance':
    dropdown_yahooExchange = st.selectbox('Select Exchange', options=['nasdaq', 'nyse', 'nysemkt'])
    start_year = st.selectbox("Start Year:", options=[str(year) for year in range(1991, 2015)])

    if 'yahoo_ticker' not in st.session_state:
        st.session_state.yahoo_ticker = []

    ticker_data = data_yfinance_ticker if 'yfinance' in locals() else pd.DataFrame()
    if not ticker_data.empty and dropdown_yahooExchange in ticker_data.columns:
        options = [stock for stock in ticker_data[dropdown_yahooExchange].dropna().tolist()]
    else:
        options = []

    if st.button('Choose Random Stocks'):
        st.session_state.yahoo_ticker = random.sample(options, min(30, len(options)))

    yahoo_ticker = st.multiselect(
        'Select up to 30 Stocks', options,
        default=st.session_state.yahoo_ticker[:30] if st.session_state.yahoo_ticker else []
    )

    if len(yahoo_ticker) > 30:
        st.error("You can only select up to 30 stocks")
    elif len(yahoo_ticker) == 30:
        st.success("30 stocks selected. Preparing data...")

# Handle other sources
elif dropdown_dataSource in ['Stooq', 'Tiingo', 'Alphavantage']:
    st.text_input(f'Enter 30 {dropdown_dataSource} stock symbols (comma separated)')

# Process Data
if st.button("Create Test Data"):
    if dropdown_dataSource == 'Yahoo Finance' and len(yahoo_ticker) == 30:
        portfolio_data = []
        portfolio_ticker = []

        for ticker in yahoo_ticker:
            try:
                stock_data = yf.download(ticker, period="max")
                if not stock_data.empty and len(stock_data) > 100:
                    portfolio_data.append(stock_data['Close'])
                    portfolio_ticker.append(ticker)
            except Exception as e:
                st.error(f"Error fetching {ticker}: {e}")

        if len(portfolio_data) == 30:
            combined_data = pd.concat(portfolio_data, axis=1, keys=portfolio_ticker)
            combined_data.dropna(how='all', inplace=True)
            st.write(combined_data)
            if st.button("Connect to QuantGenius AI engine"):
                st.success("Connected successfully!")
        else:
            st.error(f"Data is incomplete, only {len(portfolio_data)} stocks retrieved.")
    else:
        st.error("Please select 30 stocks.")

# Footer
st.markdown("""
    <p style='font-size: 12px;'>
        - Learn more about this testing <a href='https://www.kompas.com' target='_blank'>here</a><br>
        - You can check HTTP network interactions with QuantGenius via browser inspect.
    </p>
""", unsafe_allow_html=True)
