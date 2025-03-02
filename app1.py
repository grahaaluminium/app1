import streamlit as st
import time
import pandas as pd
import numpy as np
import random
import datetime as dt
import yfinance as yf

data_stooq_ticker = pd.read_csv('https://raw.githubusercontent.com/guangyoung/dataStock/refs/heads/main/stooq_tickers.csv')
data_yfinance_ticker = pd.read_csv('https://raw.githubusercontent.com/guangyoung/dataStock/refs/heads/main/stooq_tickers.csv')

st.markdown("<div style='text-align: center; margin-top: -53px;'><img src='{}' width='120'></div>".format('https://e7.pngegg.com/pngimages/589/237/png-clipart-orange-and-brown-ai-logo-area-text-symbol-adobe-ai-text-trademark-thumbnail.png'), unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-top: 10px; font-size: 18px;'>Test me using any stock from any data source, any exchange, over any period.</p>", unsafe_allow_html=True)

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
        # Dropdown 1
        dropdown_1 = st.selectbox('Initial Equity', options=[1000000, 2000000, 3000000, 4000000])        
        # Dropdown 2
        dropdown_2 = st.selectbox('Commision per trade', options=[0.001, 0.002, 0.003])        
        # Dropdown 3
        dropdown_3 = st.selectbox('Spread + Slippage per size', options=[0.001, 0.002, 0.003])        
        # Dropdown 4
        dropdown_4 = st.selectbox('Interest Rate per year', options=[0.02, 0.03, 0.04])        
        # Dropdown 5
        dropdown_5 = st.selectbox('Initial Margin Requirement', options=[0.1, 0.2, 0.3])        
        # Dropdown 6
        dropdown_6 = st.selectbox('Margin Maintenance', options=[0.1, 0.2, 0.3])

    button_jupyter = """
    <button style='padding: 2px 5px; font-size: 17px; width: 100%; border: 1px solid #ccc'>
        <img style='margin-right: 10px' src="data:image/png;base64,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" width="30" height="30" />
        Test with Jupyter Notebook
    </button>
    """

    button_colab = """
    <button style='padding: 2px 5px; font-size: 17px; width: 100%; margin-top: 10px; border: 1px solid #ccc'>
        <img style='margin-right: 10px' src="https://i0.wp.com/begincodingnow.com/wp-content/uploads/2023/08/colab_logo.png?fit=260%2C160&ssl=1" width="45" height="30" />
        Test with Google Colab
    </button>
    """

    button_github = """
    <button style='padding: 2px 5px; font-size: 17px; width: 100%; margin-top: 10px; border: 1px solid #ccc'>
        <img style='margin-right: 10px' src="data:image/jpeg;base64,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" width="30" height="30" />
        View Source Code
    </button>
    """

    st.sidebar.markdown(button_jupyter, unsafe_allow_html=True)
    st.sidebar.markdown(button_colab, unsafe_allow_html=True)
    st.sidebar.markdown(button_github, unsafe_allow_html=True)
    
# Menampilkan menu samping dengan 6 dropdown dan logo
dropdowns = sidebar_menu()

def swap():
    st.session_state.target_lang = 'Yahoo Finance'
    # st.experimental_rerun()
    
x = 0
dropdown_dataSource = st.selectbox('Select Data Source', options=['Yahoo Finance', 'Stooq', 'Tiingo', 'Alphavantage', 'Montecarlo Simulation', 'Local Data'], key="target_lang")  


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
            x = 1
elif dropdown_dataSource == 'Yahoo Finance':
    dropdown_yahooExchange = st.selectbox('Select Exchange', options=['nasdaq','nyse','nysemkt'])

    # Dropdown untuk memilih tahun mulai
    start_year = st.selectbox("Start Year:", options=[str(year) for year in range(1991, 2015)], index=0)
    
    ticker_data = data_yfinance_ticker
    options = [stock for stock in ticker_data[dropdown_yahooExchange].dropna().tolist() if dt.datetime.strptime(stock.split(',')[1], '%Y%m%d').year < int(start_year)]
    # st.write(options)


    # Membuat multiple select
    if dropdown_yahooExchange == 'nasdaq':
        
        if 'yahoo_ticker' not in st.session_state:
            st.session_state.yahoo_ticker = []
        if st.button('Choose Random Stocks'):
            st.session_state.yahoo_ticker = random.sample(options, 30)
        yahoo_ticker = st.multiselect('Select 30 Stocks or click `Choose Random Stocks` above', options, default=st.session_state.yahoo_ticker)
        # if len(yahoo_ticker) > 30:            
        #     st.error("Ticker yang anda pilih lebih dari 30")
        # elif len(yahoo_ticker) == 30:
        #     st.success("Proses selesai!")
   
elif dropdown_dataSource == 'Stooq':
    stooq_ticker = st.text_input('Masukkan 30 kode saham (dengan koma pemisah) atau klik "Random Stocks" above', placeholder = 'BBCA,BBRI,BMRI,TLKM,ASII,UNVR,PGAS,KLBF,GGRM,INDF,ACES,LPPF,CPIN,HMSP,EXCL,BDMN,MIKA,ADRO,PTPP,CTRA,WIKA,MEDC,BBNI,BIPI,BOLT,TPIA,SM')
    randomStockStooq_button = st.button("Choose Random Stocks")
elif dropdown_dataSource == 'Tiingo':
    tiingo_apikey = st.text_input('Masukkan Tiingo Api Key anda', placeholder = '1234567890abcdefghijklmnopqrstuvwxyzABCDRFGHIJKLMNOPQRSTUVWXYZ')
    tiingo_ticker = st.text_input('Masukkan 30 kode saham (dengan koma pemisah) atau klik "Random Stocks" above', placeholder = 'BBCA,BBRI,BMRI,TLKM,ASII,UNVR,PGAS,KLBF,GGRM,INDF,ACES,LPPF,CPIN,HMSP,EXCL,BDMN,MIKA,ADRO,PTPP,CTRA,WIKA,MEDC,BBNI,BIPI,BOLT,TPIA,SM')
    randomStockTiingo_button = st.button("Choose Random Stocks")
elif dropdown_dataSource == 'Alphavantage':
    alphavantage_apikey = st.text_input('Masukkan Alphavantage Api Key anda', placeholder = '1234567890abcdefghijklmnopqrstuvwxyzABCDRFGHIJKLMNOPQRSTUVWXYZ')
    alphavantage_ticker = st.text_input('Masukkan 30 kode saham (dengan koma pemisah) atau klik "Random Stocks" above', placeholder = 'BBCA,BBRI,BMRI,TLKM,ASII,UNVR,PGAS,KLBF,GGRM,INDF,ACES,LPPF,CPIN,HMSP,EXCL,BDMN,MIKA,ADRO,PTPP,CTRA,WIKA,MEDC,BBNI,BIPI,BOLT,TPIA,SM')
    randomStockAlphavantage_button = st.button("Choose Random Stocks")

test_button = st.button("Connect to QuantGenius AI engine for real-time trade signals")

n=0

if test_button:
    st.write(len(yahoo_ticker))
    if len(yahoo_ticker) == 30:
        portfolio_data, portfolio_ticker = [], []
        if dropdown_dataSource == 'Yahoo Finance':
            for ticker in yahoo_ticker:
                st.write(ticker.split(',')[0])
                ticker_data = yf.download(ticker.split(',')[0], period="max")
                if len(ticker_data) > 100 and ticker not in portfolio_ticker:
                    ticker_data.set_index(pd.to_datetime(ticker_data['Date']), inplace=True)
                    portfolio_data.append(ticker_data['Close'])
                    portfolio_ticker.append(ticker)
                    st.write(ticker_data)
                else:
                    st.write(ticker)
        elif dropdown_dataSource == 'local':
            uploaded_files = st.file_uploader("Upload File From Local Computer:", type=['csv'], accept_multiple_files=True)
            for uploaded_file in uploaded_files:
                ticker_data = pd.read_csv(uploaded_file)
                ticker_data.set_index(pd.to_datetime(ticker_data['Date']), inplace=True)
                ticker = uploaded_file.name.rsplit('.', 1)[0]
                if len(ticker_data) > 0 and ticker not in portfolio_ticker:
                    portfolio_data.append(ticker_data['Close'])
                    portfolio_ticker.append(ticker)
        st.write(portfolio_data)
        if len(portfolio_data) >= 5:
            test_start_date = max([data.index.min() for data in portfolio_data])
            st.write(test_start_date)
            test_end_date = min([data.index.max() for data in portfolio_data])
            st.write(test_end_date)
            date_range = pd.date_range(test_start_date, test_end_date)
            date_range = date_range[~date_range.weekday.isin([5, 6])]
            test_data = pd.DataFrame([
                [data.loc[test_date] if test_date in data.index else data.loc[:test_date].iloc[-1] for data in portfolio_data]
                for test_date in date_range
            ], index=date_range.date)
            st.write(test_data)
    
            st.button("Reset", on_click=swap)
    else:
        error_message = st.error("Portfolio data anda belum ada atau belum dibuat !")    
        # Tunggu beberapa detik sebelum menghapus pesan
        time.sleep(3)  # Waktu tunggu 3 detik
        error_message.empty()  # Menghapus pesan error

st.markdown("<p style='text-align: left; margin-top: 0px; font-size: 12px;'><i>- Learn more about this testing or how to use me in real trade<br>- Anda bisa mengecek HTTP network antara anda dan QuantGenius dengan mengklik tombol kana dan pilih inspect. <a href='https://www.kompas.com' target='_blank'>Learn more</a><br>- Anda bisa mengecek HTTP network anatar anda dan QuantGenius dengan mengklik tombol kana dan pilih inspect</i></p>", unsafe_allow_html=True)





