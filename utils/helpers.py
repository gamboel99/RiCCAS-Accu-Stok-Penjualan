import pandas as pd

def load_data(path, columns):
    ["Tanggal", "Kode", "Nama", "Qty", "Harga Jual", "Diskon"]
    
def save_data(df, path):
    df.to_csv(path, index=False)

def calculate_summary(stok_path, penjualan_path):
    stok = pd.read_csv(stok_path)
    jual = pd.read_csv(penjualan_path)

    # Pastikan kolom-kolom penting selalu ada
    for col in ["Qty", "Harga Jual", "Diskon"]:
        if col not in jual.columns:
            jual[col] = 0

    # Hitung Subtotal: (Qty × Harga Jual) - Diskon
    jual["Subtotal"] = (jual["Qty"] * jual["Harga Jual"]) - jual["Diskon"]

    # Total Penjualan
    total_penjualan = jual["Subtotal"].sum()

    # Total Modal dari stok terakhir (berdasarkan Kode dan Nama)
    if not stok.empty:
        latest_stok = stok.sort_values("Tanggal").drop_duplicates(["Kode", "Nama"], keep="last")
        merged = pd.merge(jual, latest_stok, on=["Kode", "Nama"], how="left", suffixes=("", "_stok"))
        merged["Harga Modal"] = merged["Harga Modal"].fillna(0)
        merged["Modal"] = merged["Qty"] * merged["Harga Modal"]
        total_modal = merged["Modal"].sum()
    else:
        total_modal = 0

    laba_kotor = total_penjualan - total_modal

    return {
        "Total Penjualan": total_penjualan,
        "Total Modal": total_modal,
        "Laba Kotor": laba_kotor
    }

def analyze_product_sales(stok_path, jual_path):
    stok = pd.read_csv(stok_path)
    jual = pd.read_csv(jual_path)

    if stok.empty or jual.empty:
        return pd.DataFrame([{"Pesan": "Belum ada cukup data"}])

    # Rekap total barang masuk
    stok_summary = stok.groupby(["Kode", "Nama", "Jenis Kendaraan", "Merek"]).agg({
        "Qty": "sum",
        "Harga Modal": "mean"
    }).rename(columns={"Qty": "Total Masuk"})

    # Rekap total terjual
    jual_summary = jual.groupby(["Kode", "Nama"]).agg({
        "Qty": "sum"
    }).rename(columns={"Qty": "Total Terjual"})

    # Gabungkan
    result = pd.merge(stok_summary, jual_summary, on=["Kode", "Nama"], how="left").fillna(0)
    result["Stok Akhir"] = result["Total Masuk"] - result["Total Terjual"]

    # Analisa performa
    result["Status"] = result["Total Terjual"].apply(
        lambda x: "Cepat Habis" if x >= 10 else "Kurang Laku"
    )

    return result.reset_index()
