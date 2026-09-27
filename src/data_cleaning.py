from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Walmart_DataSet.csv"
OUT = ROOT / "data" / "processed" / "walmart_cleaned.csv"

df = pd.read_csv(RAW)
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

assert df["Weekly_Sales"].ge(0).all()
assert df["Store"].nunique() == 45
assert df.isna().sum().sum() == 0

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.month_name()
df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
df["Year_Month"] = df["Date"].dt.to_period("M").astype(str)
df["Holiday"] = df["Holiday_Flag"].map({0: "Non-Holiday", 1: "Holiday"})
df["Sales_Million"] = df["Weekly_Sales"] / 1_000_000

OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT, index=False)
print(f"Saved {len(df):,} rows to {OUT}")