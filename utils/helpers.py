
import pandas as pd
import os

def load_data(filepath, columns):
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame(columns=columns)

def save_data(df, filepath):
    df.to_csv(filepath, index=False)

def calculate_summary(stok_path, jual_path):
    if not os.path.exists(stok_path) or not os.path.exists(jual_path):
        return pd.DataFrame()

    stok = pd.read_csv(stok_path)
    jual = pd.read_csv(jual_path)

    stok_summary = stok.groupby("Kode").agg({'Qty': 'sum', 'Harga Modal': 'mean'}).reset_index()
    jual_summary = jual.groupby("Kode").agg({'Qty': 'sum', 'Harga Jual': 'mean'}).reset_index()

    merged = pd.merge(jual_summary, stok_summary, on="Kode", how="left", suffixes=("_jual", "_modal"))
    merged["Pendapatan"] = merged["Qty_jual"] * merged["Harga Jual"]
    merged["Modal"] = merged["Qty_jual"] * merged["Harga Modal"]
    merged["Laba"] = merged["Pendapatan"] - merged["Modal"]
    merged["Status"] = merged["Laba"].apply(lambda x: "Untung" if x > 0 else ("Rugi" if x < 0 else "Stagnan"))

    return merged[["Kode", "Qty_jual", "Harga Jual", "Harga Modal", "Pendapatan", "Modal", "Laba", "Status"]]
