import streamlit as st
import time
import pandas as pd
import numpy as np
import random
import datetime as dt
import yfinance as yf

# Load ticker data
data_stooq_ticker = pd.read_csv('https://raw.githubusercontent.com/guangyoung/dataStock/refs/heads/main/stooq_tickers.csv')
data_yfinance_ticker = pd.read_csv('https://raw.githubusercontent.com/guangyoung/dataStock/refs/heads/main/stooq_tickers.csv')

# UI Setup
st.markdown("<div style='text-align: center; margin-top: -53px;'><img src='{}' width='120'></div>".format('https://e7.pngegg.com/pngimages/589/237/png-clipart-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-thumbnail.png'), unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: 10px; font-size: 18px;'>Test me using any stock from any data source, any exchange, over any period.</p>", unsafe_allow_html=True)

# Sidebar Menu
def sidebar_menu():
    st.sidebar.markdown("<div style='text-align: center; margin-top: -60px;'><img src='{}' width='150'></div>".format('https://e7.pngegg.com/pngimages/589/237/png-clipart-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-thumbnail.png'), unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;margin-top: 0px;font-size: 30px'><b>QUANTGENIUS</b></p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;margin-top: -20px;font-size: 20px'>Artificial Superintelligence Quantitative Trading System</p>", unsafe_allow_html=True)
  
    with st.sidebar.expander("Input your QuantGenius API Key", expanded=False):
        api_key1 = st.text_input("Enter your QuantGenius API Key1", type="password")
        if api_key1:
            st.success("QuantGenius API Key successfully entered!")
        st.markdown("<p style='margin-top: 0px;font-size: 12px'>Don't have QuantGenius API Key, please <a href='https://www.kompas.com' target='_blank'>click here</a></p>", unsafe_allow_html=True)
        
    with st.sidebar.expander("Setting your test parameter", expanded=False):
        dropdown_1 = st.selectbox('Initial Equity', options=[1000000, 2000000, 3000000, 4000000])        
        dropdown_2 = st.selectbox('Commision per trade', options=[0.001, 0.002, 0.003])        
        dropdown_3 = st.selectbox('Spread + Slippage per size', options=[0.001, 0.002, 0.003])        
        dropdown_4 = st.selectbox('Interest Rate per year', options=[0.02, 0.03, 0.04])        
        dropdown_5 = st.selectbox('Initial Margin Requirement', options=[0.1, 0.2, 0.3])        
        dropdown_6 = st.selectbox('Margin Maintenance', options=[0.1, 0.2, 0.3])

# Display sidebar
sidebar_menu()

def swap():
    st.session_state.target_lang = 'Yahoo Finance'
    st.session_state.yahoo_ticker = []

# Data Source Selection
dropdown_dataSource = st.selectbox('Select Data Source', options=['Yahoo Finance', 'Stooq', 'Tiingo', 'Alphavantage', 'Montecarlo Simulation', 'Local Data'], key="target_lang")  

# Handle Local Data
if dropdown_dataSource == 'Local Data':
    uploaded_files = st.file_uploader("Choose 30 stock file for your portfolio", type=["txt", "csv"], accept_multiple_files=True)
    st.session_state.uploaded_files = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name in st.session_state.uploaded_files:
                st.session_state.uploaded_files.remove(uploaded_file.name)
                st.error(f"File dengan nama '{uploaded_file.name}' sudah ada!, buang file tersebut")
            else:
                st.session_state.uploaded_files.append(uploaded_file.name)
        if len(uploaded_files) < 4:
            st.write(f"Total file yang dipilih kurang {4-len(uploaded_files)} file")
        else:
            st.success("Proses selesai!")

# Handle Yahoo Finance
elif dropdown_dataSource == 'Yahoo Finance':
    dropdown_yahooExchange = st.selectbox('Select Exchange', options=['nasdaq', 'nyse', 'nysemkt'])
    
    # Dropdown untuk memilih tahun mulai
    start_year = st.selectbox("Start Year:", options=[str(year) for year in range(1991, 2015)], index=0, key="start_year")
    
    # Reset session state jika start_year berubah
    if "previous_start_year" not in st.session_state:
        st.session_state.previous_start_year = start_year
    if st.session_state.previous_start_year != start_year:
        st.session_state.yahoo_ticker = []  # Reset session state
        st.session_state.previous_start_year = start_year  # Update previous_start_year
    
    # Filter options based on start year
    ticker_data = data_yfinance_ticker
    options = [stock for stock in ticker_data[dropdown_yahooExchange].tolist() if dt.datetime.strptime(stock.split(',')[1], '%Y%m%d').year < int(start_year)]
    
    # Initialize session state for yahoo_ticker
    if 'yahoo_ticker' not in st.session_state:
        st.session_state.yahoo_ticker = []
    
    # Random stock selection
    if st.button('Choose Random Stocks'):
        st.session_state.yahoo_ticker = random.sample(options, 30)
    
    # Multiselect widget with validated default values
    default_tickers = [ticker for ticker in st.session_state.yahoo_ticker if ticker in options]
    yahoo_ticker = st.multiselect('Select 30 Stocks or click `Choose Random Stocks` above', options, default=default_tickers)
    
    # Validate selection
    if len(yahoo_ticker) > 30:
        st.error("Ticker yang anda pilih lebih dari 30")
    elif len(yahoo_ticker) == 30:
        st.success("30 saham telah dipilih, mohon tunggu proses reconstruct data!")

# Handle other data sources
elif dropdown_dataSource == 'Stooq':
    stooq_ticker = st.text_input('Masukkan 30 kode saham (dengan koma pemisah) atau klik "Random Stocks" above', placeholder='BBCA,BBRI,BMRI,TLKM,ASII,UNVR,PGAS,KLBF,GGRM,INDF,ACES,LPPF,CPIN,HMSP,EXCL,BDMN,MIKA,ADRO,PTPP,CTRA,WIKA,MEDC,BBNI,BIPI,BOLT,TPIA,SM')
    randomStockStooq_button = st.button("Choose Random Stocks")

elif dropdown_dataSource == 'Tiingo':
    tiingo_apikey = st.text_input('Masukkan Tiingo Api Key anda', placeholder='1234567890abcdefghijklmnopqrstuvwxyzABCDRFGHIJKLMNOPQRSTUVWXYZ')
    tiingo_ticker = st.text_input('Masukkan 30 kode saham (dengan koma pemisah) atau klik "Random Stocks" above', placeholder='BBCA,BBRI,BMRI,TLKM,ASII,UNVR,PGAS,KLBF,GGRM,INDF,ACES,LPPF,CPIN,HMSP,EXCL,BDMN,MIKA,ADRO,PTPP,CTRA,WIKA,MEDC,BBNI,BIPI,BOLT,TPIA,SM')
    randomStockTiingo_button = st.button("Choose Random Stocks")

elif dropdown_dataSource == 'Alphavantage':
    alphavantage_apikey = st.text_input('Masukkan Alphavantage Api Key anda', placeholder='1234567890abcdefghijklmnopqrstuvwxyzABCDRFGHIJKLMNOPQRSTUVWXYZ')
    alphavantage_ticker = st.text_input('Masukkan 30 kode saham (dengan koma pemisah) atau klik "Random Stocks" above', placeholder='BBCA,BBRI,BMRI,TLKM,ASII,UNVR,PGAS,KLBF,GGRM,INDF,ACES,LPPF,CPIN,HMSP,EXCL,BDMN,MIKA,ADRO,PTPP,CTRA,WIKA,MEDC,BBNI,BIPI,BOLT,TPIA,SM')
    randomStockAlphavantage_button = st.button("Choose Random Stocks")

if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False
# Connect to QuantGenius AI Engine
# createData_button = st.button("Create Test Data", disabled=st.session_state.button_disabled)

if st.button("Create Test Data", disabled=st.session_state.button_disabled == True):
    # st.session_state.button_disabled = True
    if dropdown_dataSource == 'Yahoo Finance' and len(yahoo_ticker) == 30:
        portfolio_data, portfolio_ticker = [], []
        for ticker in yahoo_ticker:
            try:
                ticker_data = yf.download(ticker.split('.')[0], period="max")
                if len(ticker_data) > 100 and ticker not in portfolio_ticker:
                    portfolio_data.append(ticker_data['Close'][ticker.split('.')[0].upper()])
                    portfolio_ticker.append(ticker)
            except Exception as e:
                st.error(f"Error downloading data for {ticker}: {e}")
        
        if len(portfolio_data) == 30:
            test_start_date = max([data.index.min() for data in portfolio_data])
            test_end_date = min([data.index.max() for data in portfolio_data])
            date_range = pd.date_range(test_start_date, test_end_date)
            date_range = date_range[~date_range.weekday.isin([5, 6])]
            test_data = pd.DataFrame([
                [data.loc[test_date] if test_date in data.index else data.loc[:test_date].iloc[-1] for data in portfolio_data]
                for test_date in date_range
            ], index=date_range.date)
            st.write(test_data)
            st.session_state.button_disabled = False

            test_button = st.button("Connect to QuantGenius AI engine for real-time trade signals")

            if test_button:
                st.success("Proses selesai!")
                st.button("Reset", on_click=swap)
        else:
            st.error(f"Portfolio data anda belum kurang {30-len(portfolio_data)} !")
            st.session_state.button_disabled = False
    else:
        st.error("Portfolio data anda belum ada atau belum dibuat !")
        st.session_state.button_disabled = False

# Footer
st.markdown("<p style='text-align: left; margin-top: 0px; font-size: 12px;'><i>- Learn more about this testing or how to use me in real trade<br>- Anda bisa mengecek HTTP network antara anda dan QuantGenius dengan mengklik tombol kana dan pilih inspect. <a href='https://www.kompas.com' target='_blank'>Learn more</a><br>- Anda bisa mengecek HTTP network anatar anda dan QuantGenius dengan mengklik tombol kana dan pilih inspect</i></p>", unsafe_allow_html=True)
