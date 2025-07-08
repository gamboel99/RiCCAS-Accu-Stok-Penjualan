
import streamlit as st
import pandas as pd
import os
from utils.helpers import load_data, save_data, calculate_summary

st.set_page_config(page_title="RiCCAS Accu - Sistem Stok & Penjualan", layout="wide")
st.title("📦 RiCCAS Accu - Sistem Stok & Penjualan")

tab1, tab2, tab3 = st.tabs(["📥 Stok", "🛒 Penjualan", "📊 Laporan"])

with tab1:
    st.header("Input / Update Stok")
    stock_df = load_data("data/stok.csv", ["Tanggal", "Kode", "Nama", "Qty", "Harga Modal"])
    st.dataframe(stock_df, use_container_width=True)
    if st.button("💾 Simpan Data Stok"):
        save_data(stock_df, "data/stok.csv")
        st.success("Data stok disimpan.")

with tab2:
    st.header("Input Penjualan")
    sales_df = load_data("data/penjualan.csv", ["Tanggal", "Kode", "Nama", "Qty", "Harga Jual"])
    st.dataframe(sales_df, use_container_width=True)
    if st.button("💾 Simpan Data Penjualan"):
        save_data(sales_df, "data/penjualan.csv")
        st.success("Data penjualan disimpan.")

with tab3:
    st.header("Laporan Penjualan & Status Usaha")
    summary = calculate_summary("data/stok.csv", "data/penjualan.csv")
    st.dataframe(summary, use_container_width=True)
