import streamlit as st
import pandas as pd
import os
from datetime import datetime
from utils.helpers import load_data, save_data, calculate_summary, analyze_product_sales

st.set_page_config(page_title="RiCCAS Accu - Sistem Stok & Penjualan", layout="wide")
st.title("📦 RiCCAS Accu - Sistem Stok & Penjualan")

# Path file
stok_path = "data/stok.csv"
penjualan_path = "data/penjualan.csv"
kode_barang_path = "data/kode_barang.csv"

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📥 Input Stok", "🛒 Penjualan", "📊 Laporan", "📌 Analisa Produk"])

# ================= TAB 1 - INPUT STOK =================
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
                nama = kode_barang_df[kode_barang_df["Kode"] == kode]["Nama"].values[0]
                jenis = kode_barang_df[kode_barang_df["Kode"] == kode]["Jenis Kendaraan"].values[0]
                st.text_input("Nama Barang", nama, disabled=True)
                st.text_input("Jenis Kendaraan", jenis, disabled=True)
            with col2:
                merek = st.text_input("Merek")
                qty = st.number_input("Jumlah Masuk", min_value=0)
                harga_modal = st.number_input("Harga Modal per Unit", min_value=0)

            submitted = st.form_submit_button("💾 Tambah ke Stok")
            if submitted:
                df = load_data(stok_path, ["Tanggal", "Kode", "Nama", "Jenis Kendaraan", "Merek", "Qty", "Harga Modal"])
                new_row = pd.DataFrame([{
                    "Tanggal": tanggal,
                    "Kode": kode,
                    "Nama": nama,
                    "Jenis Kendaraan": jenis,
                    "Merek": merek,
                    "Qty": qty,
                    "Harga Modal": harga_modal
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df, stok_path)
                st.success("✅ Data stok berhasil ditambahkan!")
    else:
        st.warning("❗ File kode_barang.csv tidak ditemukan!")

    st.subheader("📋 Data Stok Saat Ini")
    st.dataframe(load_data(stok_path, ["Tanggal", "Kode", "Nama", "Jenis Kendaraan", "Merek", "Qty", "Harga Modal"]), use_container_width=True)

# ================= TAB 2 - PENJUALAN =================
with tab2:
    st.header("Form Input Penjualan")
    if os.path.exists(kode_barang_path):
        kode_barang_df = pd.read_csv(kode_barang_path)
        kode_list = kode_barang_df["Kode"].tolist()

        with st.form("form_penjualan"):
            col1, col2 = st.columns(2)
            with col1:
                tanggal = st.date_input("Tanggal Jual", value=datetime.today())
                kode = st.selectbox("Kode Barang Terjual", kode_list)
                nama = kode_barang_df[kode_barang_df["Kode"] == kode]["Nama"].values[0]
                st.text_input("Nama Barang", nama, disabled=True)
            with col2:
                qty = st.number_input("Jumlah Terjual", min_value=0)
                harga_jual = st.number_input("Harga Jual per Unit", min_value=0)

            submitted2 = st.form_submit_button("💾 Tambah ke Penjualan")
            if submitted2:
                columns = ["Tanggal", "Kode", "Nama", "Qty", "Harga Jual"]
                df = load_data(penjualan_path, columns)
                new_row = pd.DataFrame([{
                    "Tanggal": tanggal,
                    "Kode": kode,
                    "Nama": nama,
                    "Qty": qty,
                    "Harga Jual": harga_jual
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df, penjualan_path)
                st.success("✅ Data penjualan berhasil ditambahkan!")
    else:
        st.warning("❗ File kode_barang.csv tidak ditemukan!")

    st.subheader("🧾 Data Penjualan")
    st.dataframe(load_data(penjualan_path, ["Tanggal", "Kode", "Nama", "Qty", "Harga Jual"]), use_container_width=True)

# ================= TAB 3 - LAPORAN =================
with tab3:
    st.header("📊 Laporan Keuangan Sederhana")
    summary = calculate_summary(stok_path, penjualan_path)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Penjualan (Rp)", f"{summary['Total Penjualan']:,.0f}")
    col2.metric("Total Modal (Rp)", f"{summary['Total Modal']:,.0f}")
    col3.metric("Laba Kotor (Rp)", f"{summary['Laba Kotor']:,.0f}")

# ================= TAB 4 - ANALISA PRODUK =================
with tab4:
    st.header("📌 Analisa Performa Produk")
    analisa = analyze_product_sales(stok_path, penjualan_path)
    st.dataframe(analisa, use_container_width=True)
import io
from openpyxl import Workbook

# Tombol Simpan Excel
st.sidebar.header("📁 Export Data")
if st.sidebar.button("📤 Download Excel (.xlsx)"):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')

    # Load semua data
    df_stok = load_data(stok_path, ["Tanggal", "Kode", "Nama", "Jenis Kendaraan", "Merek", "Qty", "Harga Modal"])
    df_penjualan = load_data(penjualan_path, ["Tanggal", "Kode", "Nama", "Qty", "Harga Jual"])
    df_analisa = analyze_product_sales(stok_path, penjualan_path)

    # Ringkasan keuangan
    summary = calculate_summary(stok_path, penjualan_path)
    df_summary = pd.DataFrame([summary])

    # Tulis ke Excel
    df_stok.to_excel(writer, sheet_name="Stok", index=False)
    df_penjualan.to_excel(writer, sheet_name="Penjualan", index=False)
    df_summary.to_excel(writer, sheet_name="Ringkasan", index=False)
    df_analisa.to_excel(writer, sheet_name="Analisa", index=False)

    writer.close()
    output.seek(0)

    st.sidebar.download_button(
        label="⬇️ Simpan File Excel",
        data=output,
        file_name="RiCCAS_Accu_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
