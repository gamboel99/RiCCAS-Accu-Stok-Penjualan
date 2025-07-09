import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.helpers import load_data, save_data, calculate_summary, analyze_product_sales

st.set_page_config(page_title="RiCCAS Accu - Sistem Stok & Penjualan", layout="wide")
st.title("📦 RiCCAS Accu - Sistem Stok & Penjualan")

stok_path = "data/stok.csv"
penjualan_path = "data/penjualan.csv"
kode_barang_path = "data/kode_barang.csv"

tab1, tab2, tab3, tab4 = st.tabs(["📥 Input Stok", "🛒 Penjualan", "📊 Laporan", "📌 Analisa Produk"])

with tab1:
    st.header("Form Input Stok Barang")
    if os.path.exists(kode_barang_path):
        kode_barang_df = pd.read_csv(kode_barang_path)
        kode_list = kode_barang_df["Kode"].tolist()

        with st.form("form_stok"):
            col1, col2 = st.columns(2)
            with col1:
                tanggal = st.date_input("Tanggal", value=datetime.today())
                kode = st.selectbox("Kode Barang", kode_list)
                match = kode_barang_df[kode_barang_df["Kode"] == kode].iloc[0]
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
                df = load_data(stok_path, ["Tanggal", "Kode", "Nama", "Jenis Kendaraan", "Merek", "Qty", "Harga Modal"])
                new_row = {
                    "Tanggal": tanggal,
                    "Kode": kode,
                    "Nama": nama,
                    "Jenis Kendaraan": jenis,
                    "Merek": merek,
                    "Qty": qty,
                    "Harga Modal": harga_modal
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df, stok_path)
                st.success("✅ Data stok berhasil ditambahkan!")
    else:
        st.warning("❗ File kode_barang.csv tidak ditemukan!")

    st.subheader("📋 Data Stok Saat Ini")
    st.dataframe(load_data(stok_path, ["Tanggal", "Kode", "Nama", "Jenis Kendaraan", "Merek", "Qty", "Harga Modal"]), use_container_width=True)

with tab2:
    st.header("Form Input Penjualan")
    with st.form("form_penjualan"):
        col1, col2 = st.columns(2)
        with col1:
            tanggal = st.date_input("Tanggal Jual", value=datetime.today())
            kode = st.text_input("Kode Barang Terjual")
            nama = st.text_input("Nama Barang")
        with col2:
            qty = st.number_input("Jumlah Terjual", min_value=0)
            harga_jual = st.number_input("Harga Jual per Unit", min_value=0)
            diskon = st.number_input("Diskon (Rp)", min_value=0)
        submitted2 = st.form_submit_button("💾 Tambah ke Penjualan")
        if submitted2:

    submitted2 = st.form_submit_button("💾 Tambah ke Penjualan")
if submitted2:
    columns = ["Tanggal", "Kode", "Nama", "Qty", "Harga Jual", "Diskon"]
    
    df = load_data(penjualan_path, columns)

    # Buat new_row sebagai DataFrame sesuai struktur
    new_row = pd.DataFrame([{
        "Tanggal": tanggal,
        "Kode": kode,
        "Nama": nama,
        "Qty": qty,
        "Harga Jual": harga_jual,
        "Diskon": diskon
    }], columns=columns)

    # Pastikan df memiliki kolom yang sama
    for col in columns:
        if col not in df.columns:
            df[col] = None

    # Tambahkan baris baru
    df = pd.concat([df[columns], new_row], ignore_index=True)

    save_data(df, penjualan_path)
    st.success("✅ Data penjualan berhasil ditambahkan!")

with tab3:
    st.header("📊 Laporan Keuangan Sederhana")
    summary = calculate_summary(stok_path, penjualan_path)
    st.metric("Total Penjualan (Rp)", f"{summary['Total Penjualan']:,.0f}")
    st.metric("Total Modal (Rp)", f"{summary['Total Modal']:,.0f}")
    st.metric("Laba Kotor (Rp)", f"{summary['Laba Kotor']:,.0f}")

with tab4:
    st.header("📌 Analisa Performa Produk")
    analisa = analyze_product_sales(stok_path, penjualan_path)
    st.dataframe(analisa, use_container_width=True)
