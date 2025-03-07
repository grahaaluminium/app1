import streamlit as st
import pandas as pd
import random
import datetime as dt
import yfinance as yf

# Load ticker data
ticker_data = pd.read_csv('https://raw.githubusercontent.com/guangyoung/dataStock/refs/heads/main/stooq_tickers.csv')

# UI Setup
st.markdown("<div style='text-align: center; margin-top: -40px;'><img src='{}' width='120'></div>".format('https://e7.pngegg.com/pngimages/589/237/png-clipart-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-thumbnail.png'), unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: 10px; font-size: 18px;'>Test me using any stock from any data source, any exchange, over any period.</p>", unsafe_allow_html=True)

# Sidebar Menu
def sidebar_menu():
    st.sidebar.markdown("<div style='text-align: center; margin-top: -60px;'><img src='{}' width='150'></div>".format('https://e7.pngegg.com/pngimages/589/237/png-clipart-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-thumbnail.png'), unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;margin-top: 0px;font-size: 30px'><b>QUANTGENIUS</b></p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center;margin-top: -20px;font-size: 20px'>Artificial Superintelligence Quantitative Trading System</p>", unsafe_allow_html=True)
  
    with st.sidebar.expander("Input your QuantGenius API Key", expanded=False):
        api_key1 = st.text_input("Enter your QuantGenius API Key1", type="password")
        if api_key1:
            if len(api_key1) == 32:  # Contoh validasi sederhana
                st.session_state.api_key1 = api_key1
                st.success("QuantGenius API Key successfully entered!")
            else:
                st.error("Invalid API Key format. Please check your key.")
        st.markdown("<p style='margin-top: 0px;font-size: 12px'>Don't have QuantGenius API Key, please <a href='https://www.kompas.com' target='_blank'>click here</a></p>", unsafe_allow_html=True)
        
    with st.sidebar.expander("Setting your test parameter", expanded=False):
        st.session_state.initial_equity = st.selectbox('Initial Equity', options=[1000000, 2000000, 3000000, 4000000])        
        st.session_state.commission = st.selectbox('Commission per trade', options=[0.001, 0.002, 0.003])        
        st.session_state.spread = st.selectbox('Spread + Slippage per size', options=[0.001, 0.002, 0.003])        
        st.session_state.interest_rate = st.selectbox('Interest Rate per year', options=[0.02, 0.03, 0.04])        
        st.session_state.initial_margin = st.selectbox('Initial Margin Requirement', options=[0.1, 0.2, 0.3])        
        st.session_state.margin_maintenance = st.selectbox('Margin Maintenance', options=[0.1, 0.2, 0.3])

# Display sidebar
sidebar_menu()

def swap():
    st.session_state.target_lang = 'Yahoo Finance'   
    if 'yahoo_ticker' in st.session_state:
        del st.session_state.yahoo_ticker 

# Data Source Selection
dropdown_dataSource = st.selectbox('Select Data Source', options=['Yahoo Finance', 'Stooq', 'Tiingo', 'Alphavantage', 'Montecarlo Simulation', 'Local Data'], key="target_lang")  

# Handle Local Data
if dropdown_dataSource == 'Local Data':
    uploaded_files = st.file_uploader("Choose 30 stock file for your portfolio", type=["txt", "csv"], accept_multiple_files=True)
    if uploaded_files:
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = []
        
        for uploaded_file in uploaded_files:
            if uploaded_file.name in st.session_state.uploaded_files:
                st.error(f"File dengan nama '{uploaded_file.name}' sudah ada! Silakan buang file tersebut.")
            else:
                st.session_state.uploaded_files.append(uploaded_file.name)
        
        if len(uploaded_files) < 4:
            st.warning(f"Total file yang dipilih kurang {4 - len(uploaded_files)} file.")
        else:
            st.success("Proses selesai!")

# Handle Yahoo Finance
elif dropdown_dataSource == 'Yahoo Finance':
    dropdown_yahooExchange = st.selectbox('Select Exchange', options=['nasdaq', 'nyse', 'nysemkt'])
    
    start_year = st.selectbox("Start Year:", options=[str(year) for year in range(1991, 2015)], index=0, key="start_year")
    
    if "previous_start_year" not in st.session_state:
        st.session_state.previous_start_year = start_year
    if st.session_state.previous_start_year != start_year:
        st.session_state.yahoo_ticker = []
        st.session_state.previous_start_year = start_year
    
    options = [stock for stock in ticker_data[dropdown_yahooExchange].tolist() if dt.datetime.strptime(stock.split(',')[1], '%Y%m%d').year < int(start_year)]
    
    if 'yahoo_ticker' not in st.session_state:
        st.session_state.yahoo_ticker = []
    
    if st.button('Choose Random Stocks'):
        valid_tickers = [stock for stock in ticker_data[dropdown_yahooExchange].tolist() if dt.datetime.strptime(stock.split(',')[1], '%Y%m%d').year < int(start_year)]
        st.session_state.yahoo_ticker = random.sample(valid_tickers, 30)
    
    default_tickers = [ticker for ticker in st.session_state.yahoo_ticker if ticker in options]
    yahoo_ticker = st.multiselect('Select 30 Stocks or click `Choose Random Stocks` above', options, default=default_tickers)
    
    if len(yahoo_ticker) > 30:
        st.error("Ticker yang Anda pilih lebih dari 30.")
    elif len(yahoo_ticker) == 30:
        st.success("30 saham telah dipilih, mohon tunggu proses reconstruct data!")

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

def on_button_click():
    st.session_state.button_clicked = True

createData_button = st.button("Create Test Data and Run Test", on_click=on_button_click, disabled=st.session_state.button_clicked)

if createData_button:
    if dropdown_dataSource == 'Yahoo Finance' and len(yahoo_ticker) == 30:
        portfolio_data, portfolio_ticker = [], []
        for ticker in yahoo_ticker:
            try:
                ticker_symbol = ticker.split('.')[0].upper()
                ticker_data = yf.download(ticker_symbol, period="max")
                if len(ticker_data) > 100 and ticker not in portfolio_ticker:
                    portfolio_data.append(ticker_data['Close'].rename(ticker_symbol))
                    portfolio_ticker.append(ticker)
            except Exception as e:
                st.error(f"Error downloading data for {ticker}: {e}")
        
        if len(portfolio_data) == 30:
            test_start_date = max([data.index.min() for data in portfolio_data])
            test_end_date = min([data.index.max() for data in portfolio_data])
            date_range = pd.date_range(test_start_date, test_end_date, freq='B')  # Hanya hari kerja
            test_data = pd.DataFrame({ticker: data.reindex(date_range, method='ffill') for ticker, data in zip(portfolio_ticker, portfolio_data)})
            
            st.success("Data berhasil dibuat!")
            st.write(test_data)
            st.session_state.button_clicked = False
            st.button("Reset", on_click=swap)
        else:
            st.error(f"Portfolio data Anda kurang {30 - len(portfolio_data)} saham!")
            st.session_state.button_clicked = False
    else:
        st.error("Portfolio data Anda belum ada atau belum dibuat!")
        st.session_state.button_clicked = False

# Footer
st.markdown("""
<p style='text-align: left; margin-top: 0px; font-size: 12px;'>
    <i>
        - Learn more about this testing or how to use me in real trade<br>
        - Anda bisa mengecek HTTP network antara Anda dan QuantGenius dengan mengklik tombol kanan dan pilih inspect. <a href='https://www.kompas.com' target='_blank'>Learn more</a><br>
        - Untuk bantuan lebih lanjut, hubungi <a href='mailto:support@quantgenius.com'>support@quantgenius.com</a>
    </i>
</p>
""", unsafe_allow_html=True)
