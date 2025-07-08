import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.helpers import (
    load_data, save_data, calculate_summary, analyze_product_sales
)

st.set_page_config(page_title="RiCCAS Accu - Sistem Stok & Penjualan", layout="wide")
st.title("📦 RiCCAS Accu - Sistem Stok & Penjualan")

tab1, tab2, tab3, tab4 = st.tabs(["📥 Input Stok", "🛒 Penjualan", "📊 Laporan", "📌 Analisa Produk"])

with tab1:
    st.header("Form Input Stok Barang")

    # Load master kode barang
    kode_barang_path = "data/kode_barang.csv"
    if os.path.exists(kode_barang_path):
        kode_barang_df = pd.read_csv(kode_barang_path)
        kode_list = kode_barang_df["Kode"].tolist()

        with st.form("input_stok_form"):
            col1, col2 = st.columns(2)
            with col1:
                tanggal = st.date_input("Tanggal", value=datetime.today())
                selected_kode = st.selectbox("Kode Barang", kode_list)

                match = kode_barang_df[kode_barang_df["Kode"] == selected_kode].iloc[0]
                nama = match["Nama"]
                jenis = match["Jenis Kendaraan"]

                st.text_input("Nama Barang", nama, disabled=True)
                st.text_input("Jenis Kendaraan", jenis, disabled=True)

            with col2:
                merek = st.text_input("Merek")
                qty = st.number_input("Jumlah Masuk", min_value=0)
                harga_modal = st.number_input("Harga Modal per Unit", min_value=0)

            submitted = st.form_submit_button("💾 Tambah ke Stok")
            if submitted:
                stok_df = load_data("data/stok.csv", 
                                    ["Tanggal", "Kode", "Nama", "Jenis Kendaraan", "Merek", "Qty", "Harga Modal"])
                stok_df.loc[len(stok_df)] = [tanggal, selected_kode, nama, jenis, merek, qty, harga_modal]
                save_data(stok_df, "data/stok.csv")
                st.success("✅ Data stok berhasil ditambahkan!")
    else:
        st.warning("❗ File kode_barang.csv belum ditemukan di folder data/")

    st.subheader("📋 Data Stok Saat Ini")
    st.dataframe(load_data("data/stok.csv", 
                           ["Tanggal", "Kode", "Nama", "Jenis Kendaraan", "Merek", "Qty", "Harga Modal"]), 
                 use_container_width=True)

with tab2:
    st.header("Form Input Penjualan")

    with st.form("input_penjualan_form"):
        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.date_input("Tanggal Jual", value=datetime.today())
            kode = st.text_input("Kode Barang Terjual")
            nama = st.text_input("Nama Barang")
        with col2:
            qty = st.number_input("Jumlah Terjual", min_value=0)
            harga_jual = st.number_input("Harga Jual per Unit", min_value=0)

        submitted2 = st.form_submit_button("💾 Tambah ke Penjualan")
        if submitted2:
            jual_df = load_data("data/penjualan.csv", 
                                ["Tanggal", "Kode", "Nama", "Qty", "Harga Jual"])
            jual_df.loc[len(jual_df)] = [tanggal, kode, nama, qty, harga_jual]
            save_data(jual_df, "data/penjualan.csv")
            st.success("✅ Data penjualan berhasil ditambahkan!")

    st.subheader("🧾 Data Penjualan")
    st.dataframe(load_data("data/penjualan.csv", 
                           ["Tanggal", "Kode", "Nama", "Qty", "Harga Jual"]), 
                 use_container_width=True)

with tab3:
    st.header("📊 Laporan Laba Rugi")
    summary = calculate_summary("data/stok.csv", "data/penjualan.csv")
    st.dataframe(summary, use_container_width=True)

with tab4:
    st.header("📌 Analisa Produk")
    analysis = analyze_product_sales("data/stok.csv", "data/penjualan.csv")
    st.dataframe(analysis, use_container_width=True)
