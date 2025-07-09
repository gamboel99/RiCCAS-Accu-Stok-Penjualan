
import pandas as pd

def load_data(path, columns):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame(columns=columns)

def save_data(df, path):
    df.to_csv(path, index=False)

def calculate_summary(stok_path, penjualan_path):
    stok = pd.read_csv(stok_path)
    jual = pd.read_csv(penjualan_path)

    if jual.empty:
        jual["Subtotal"] = 0
    else:
        # Hitung Subtotal: (Qty × Harga Jual) - Diskon
        jual["Subtotal"] = (jual["Qty"] * jual["Harga Jual"]) - jual["Diskon"]

    # Total Laba Kotor
    total_penjualan = jual["Subtotal"].sum()

    # Total Modal (ambil modal dari stok terakhir berdasarkan Kode)
    if not stok.empty:
        latest_stok = stok.sort_values("Tanggal").drop_duplicates(["Kode", "Merek"], keep="last")
        merged = pd.merge(jual, latest_stok, on=["Kode", "Nama"], how="left", suffixes=("", "_stok"))
        merged["Modal"] = merged["Qty"] * merged["Harga Modal"]
        total_modal = merged["Modal"].sum()
    else:
        total_modal = 0

    # Laba/Rugi
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
    
    stok_summary = stok.groupby(["Kode", "Nama", "Jenis Kendaraan"]).agg({
        "Qty": "sum"
    }).rename(columns={"Qty": "Total Masuk"})

    jual_summary = jual.groupby("Kode").agg({
        "Qty": "sum"
    }).rename(columns={"Qty": "Total Terjual"})

    result = pd.merge(stok_summary, jual_summary, on="Kode", how="left").fillna(0)
    result["Stok Akhir"] = result["Total Masuk"] - result["Total Terjual"]
    result["Status"] = result["Total Terjual"].apply(
        lambda x: "Cepat Habis" if x >= 10 else "Kurang Laku"
    )
    return result.reset_index()
