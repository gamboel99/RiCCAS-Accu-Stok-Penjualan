
import pandas as pd

def load_data(path, columns):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame(columns=columns)

def save_data(df, path):
    df.to_csv(path, index=False)

def calculate_summary(stok_path, jual_path):
    stok = pd.read_csv(stok_path)
    jual = pd.read_csv(jual_path)
    if stok.empty or jual.empty:
        return pd.DataFrame([{"Pesan": "Belum ada cukup data stok atau penjualan"}])
    
    jual["Subtotal"] = (jual["Qty"] * jual["Harga Jual"]) - jual["Diskon"]
    jual["Pajak (Rp)"] = jual["Subtotal"] * (jual["Pajak (%)"] / 100)
    jual["Total"] = jual["Subtotal"] + jual["Pajak (Rp)"]
    total_penjualan = jual["Total"].sum()

    # Estimasi modal (ambil harga rata-rata dari stok)
    avg_modal = stok.groupby("Kode")["Harga Modal"].mean().reset_index()
    merged = pd.merge(jual, avg_modal, on="Kode", how="left")
    merged["Total Modal"] = merged["Qty"] * merged["Harga Modal"]
    total_modal = merged["Total Modal"].sum()

    laba = total_penjualan - total_modal

    return pd.DataFrame([{
        "Total Penjualan": total_penjualan,
        "Total Modal": total_modal,
        "Laba Bersih": laba
    }])

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
