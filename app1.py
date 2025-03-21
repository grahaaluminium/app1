import streamlit as st
import pandas as pd
import random
import datetime as dt
import yfinance as yf
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

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
    if 'yahoo_ticker' in st.session_state:
        del st.session_state.yahoo_ticker
    if 'button_clicked' in st.session_state:
        del st.session_state.button_clicked
    if 'uploaded_files' in st.session_state:
        del st.session_state.uploaded_files

# Data Source Selection
dropdown_dataSource = st.selectbox('Select Data Source', options=['Yahoo Finance', 'Stooq', 'Tiingo', 'Alphavantage', 'Montecarlo Simulation', 'Local Data'], key="target_lang")  

# Handle Local Data
if dropdown_dataSource == 'Local Data':
    uploaded_files = st.file_uploader("Choose 30 stock file for your portfolio", type=["txt", "csv"], accept_multiple_files=True)
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name in st.session_state.uploaded_files:
                st.error(f"File dengan nama '{uploaded_file.name}' sudah ada!, buang file tersebut")
            else:
                try:
                    # Validasi file
                    df = pd.read_csv(uploaded_file)
                    st.session_state.uploaded_files.append(uploaded_file.name)
                except Exception as e:
                    st.error(f"File {uploaded_file.name} tidak valid: {e}")
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
    options = [stock for stock in ticker_data[dropdown_yahooExchange].tolist() if dt.datetime.strptime(stock.split(',')[1], '%Y%m%d').year < int(start_year)]
    
    # Initialize session state for yahoo_ticker
    if 'yahoo_ticker' not in st.session_state:
        st.session_state.yahoo_ticker = []
    
    # Random stock selection
    if st.button('Choose Random Stocks'):
        valid_tickers = [stock for stock in ticker_data[dropdown_yahooExchange].tolist() if dt.datetime.strptime(stock.split(',')[1], '%Y%m%d').year < int(start_year)]
        st.session_state.yahoo_ticker = random.sample(valid_tickers, 30)
    
    # Multiselect widget with validated default values
    default_tickers = [ticker for ticker in st.session_state.yahoo_ticker if ticker in options]
    yahoo_ticker = st.multiselect('Select 30 Stocks or click `Choose Random Stocks` above', options, default=default_tickers)
    
    # Validate selection
    if len(yahoo_ticker) > 30:
        st.error("Anda hanya dapat memilih maksimal 30 saham. Silakan hapus beberapa saham dari pilihan Anda.")
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
        label_placeholder1 = st.empty()
        progress_bar = label_placeholder1.progress(0)
        
        label_placeholder1.write("Proses pengunduhan data...")  # Label awal
        for i, ticker in enumerate(yahoo_ticker):
            try:
                ticker_data = yf.download(ticker.split('.')[0], period="max")
                if len(ticker_data) > 100 and ticker not in portfolio_ticker:
                    portfolio_data.append(ticker_data['Close'][ticker.split('.')[0].upper()])
                    portfolio_ticker.append(ticker)
            except Exception as e:
                st.error(f"Error downloading data for {ticker}: {e}")
                continue            
            progress_bar.progress(int((i + 1) / 30 * 100))  # Update progress bar
        label_placeholder1.empty()  # Menghapus label
        if len(portfolio_data) == 30:
            test_start_date = max([data.index.min() for data in portfolio_data])
            test_end_date = min([data.index.max() for data in portfolio_data])
            date_range = pd.date_range(test_start_date, test_end_date)
            date_range = date_range[~date_range.weekday.isin([5, 6])]  # Exclude weekends
            test_data = pd.DataFrame([
                [data.loc[test_date] if test_date in data.index else data.loc[:test_date].iloc[-1] for data in portfolio_data]
                for test_date in date_range
            ], index=date_range.date)
            test_data = test_data.dropna()  # Hapus baris yang mengandung NaN
            st.write(test_data)
            # st.success("Data berhasil dibuat!")   
            
            
            # Loop untuk mengupdate progress bar
            label_placeholder2 = st.empty()
            progress_bar = label_placeholder2.progress(0)
            label_placeholder2.write("Proses get signal and test trade...")  # Label awal
            for i in range(100):
                time.sleep(0.05)  # Tunggu sebentar untuk simulasi proses                
                progress_bar.progress(i + 1)  # Update progress bar
            label_placeholder2.empty()  # Menghapus label
            st.success("Proses selesai!") 
            st.session_state.button_clicked = False
            st.button("Reset", on_click=swap)   
        else:
            st.error(f"Portfolio data anda belum kurang {30-len(portfolio_data)} !")
            st.session_state.button_clicked = False
    else:
        st.error("Portfolio data anda belum ada atau belum dibuat !")
        st.session_state.button_clicked = False

# Footer
st.markdown("""
<p style='text-align: left; margin-top: 0px; font-size: 12px;'>
    <i>
        - Learn more about this testing or how to use me in real trade<br>
        - Anda bisa mengecek HTTP network antara anda dan QuantGenius dengan mengklik tombol kanan dan pilih inspect. <a href='https://www.kompas.com' target='_blank'>Learn more</a><br>
        - Anda bisa mengecek HTTP network antara anda dan QuantGenius dengan mengklik tombol kanan dan pilih inspect
    </i>
</p>
""", unsafe_allow_html=True)
