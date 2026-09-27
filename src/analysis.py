from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "walmart_cleaned.csv"
REPORT = ROOT / "reports"
REPORT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["Date"])

print("\nDATASET")
print(df.shape)
print(df.describe(include="all"))

store = (df.groupby("Store")["Weekly_Sales"]
           .agg(Total_Sales="sum", Average_Sales="mean", Sales_Std="std")
           .sort_values("Total_Sales", ascending=False))
print("\nTOP 10 STORES")
print(store.head(10))

holiday = df.groupby("Holiday")["Weekly_Sales"].agg(["count", "mean", "sum"])
print("\nHOLIDAY ANALYSIS")
print(holiday)

corr = df[["Weekly_Sales", "Temperature", "Fuel_Price", "CPI", "Unemployment"]].corr()
print("\nCORRELATION")
print(corr["Weekly_Sales"].sort_values(ascending=False))

monthly = df.groupby("Year_Month", as_index=False)["Weekly_Sales"].sum()
plt.figure(figsize=(12, 5))
sns.lineplot(data=monthly, x="Year_Month", y="Weekly_Sales")
plt.xticks(rotation=60)
plt.title("Walmart Monthly Sales Trend")
plt.tight_layout()
plt.savefig(REPORT / "monthly_sales_trend.png", dpi=150)
plt.close()

plt.figure(figsize=(9, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Sales and Economic Variable Correlations")
plt.tight_layout()
plt.savefig(REPORT / "correlation_heatmap.png", dpi=150)
plt.close()

print("\nCharts saved to reports/")