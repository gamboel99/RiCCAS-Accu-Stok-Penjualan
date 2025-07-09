import pandas as pd

def load_data(path, columns):
    try:
        df = pd.read_csv(path)
        for col in columns:
            if col not in df.columns:
                df[col] = None
        df = df[columns]
    except:
        df = pd.DataFrame(columns=columns)
    return df

def save_data(df, path):
    df.to_csv(path, index=False)

def calculate_summary(stok_path, penjualan_path):
    stok = pd.read_csv(stok_path)
    jual = pd.read_csv(penjualan_path)

    # Konversi kolom numerik
    jual["Qty"] = pd.to_numeric(jual["Qty"], errors="coerce").fillna(0)
    jual["Harga Jual"] = pd.to_numeric(jual["Harga Jual"], errors="coerce").fillna(0)

    # Hitung total penjualan
    jual["Subtotal"] = jual["Qty"] * jual["Harga Jual"]
    total_penjualan = jual["Subtotal"].sum()

    # Total modal berdasarkan Harga Modal dari stok
    if not stok.empty:
        latest_stok = stok.sort_values("Tanggal").drop_duplicates(["Kode", "Nama"], keep="last")
        merged = pd.merge(jual, latest_stok, on=["Kode", "Nama"], how="left", suffixes=("", "_stok"))
        merged["Harga Modal"] = pd.to_numeric(merged["Harga Modal"], errors="coerce").fillna(0)
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

def analyze_product_sales(stok_path, penjualan_path):
    stok = load_data(stok_path, ["Tanggal", "Kode", "Nama", "Jenis Kendaraan", "Merek", "Qty", "Harga Modal"])
    jual = load_data(penjualan_path, ["Tanggal", "Kode", "Nama", "Qty", "Harga Jual", "Diskon"])

    if stok.empty or jual.empty:
        return pd.DataFrame([{"Pesan": "Belum ada cukup data"}])

    stok_summary = stok.groupby(["Kode", "Nama", "Jenis Kendaraan", "Merek"]).agg({
        "Qty": "sum",
        "Harga Modal": "mean"
    }).rename(columns={"Qty": "Total Masuk"})

    jual_summary = jual.groupby(["Kode", "Nama"]).agg({
        "Qty": "sum"
    }).rename(columns={"Qty": "Total Terjual"})

    result = pd.merge(stok_summary, jual_summary, on=["Kode", "Nama"], how="left").fillna(0)
    result["Stok Akhir"] = result["Total Masuk"] - result["Total Terjual"]
    result["Status"] = result["Total Terjual"].apply(lambda x: "Cepat Habis" if x >= 10 else "Kurang Laku")

    return result.reset_index()
