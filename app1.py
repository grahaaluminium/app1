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
        st.selectbox('Commission per trade', options=[0.
