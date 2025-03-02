import streamlit as st
import yfinance as yf
import pandas as pd

# Judul aplikasi
st.title("Analisis Harga Penutupan Saham")

# Input untuk tiga ticker saham
ticker1 = st.text_input("Masukkan ticker saham pertama (contoh: AAPL):", "AAPL")
ticker2 = st.text_input("Masukkan ticker saham kedua (contoh: MSFT):", "MSFT")
ticker3 = st.text_input("Masukkan ticker saham ketiga (contoh: GOOGL):", "GOOGL")

# Mengambil data dari Yahoo Finance
data1 = yf.download(ticker1, start="2020-01-01", end="2023-01-01")
data2 = yf.download(ticker2, start="2020-01-01", end="2023-01-01")
data3 = yf.download(ticker3, start="2020-01-01", end="2023-01-01")

# Menentukan rentang tanggal yang mencakup semua data saham
start_date = max(data1.index.min(), data2.index.min(), data3.index.min())
end_date = min(data1.index.max(), data2.index.max(), data3.index.max())

st.write(start_date)
st.write(end_date)
# Memfilter data berdasarkan rentang tanggal yang sama
data1_filtered = data1[(data1.index >= start_date) & (data1.index <= end_date)]
data2_filtered = data2[(data2.index >= start_date) & (data2.index <= end_date)]
data3_filtered = data3[(data3.index >= start_date) & (data3.index <= end_date)]
st.write(data1_filtered['Close']['AAPL'])

# Menggabungkan data harga penutupan ke dalam satu DataFrame
closing_prices = pd.DataFrame({
    ticker1: data1_filtered['Close'],
    ticker2: data2_filtered['Close'],
    ticker3: data3_filtered['Close']
})

# Menampilkan tabel harga penutupan
st.write("Harga Penutupan Saham:")
st.dataframe(closing_prices)

# Menampilkan rentang tanggal yang digunakan
st.write(f"Rentang tanggal yang digunakan: {start_date.strftime('%Y-%m-%d')} hingga {end_date.strftime('%Y-%m-%d')}")
