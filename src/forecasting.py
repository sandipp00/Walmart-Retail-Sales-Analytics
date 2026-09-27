from pathlib import Path
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "walmart_cleaned.csv"

df = pd.read_csv(DATA, parse_dates=["Date"])
weekly = df.groupby("Date")["Weekly_Sales"].sum().sort_index()

test_size = 12
train = weekly.iloc[:-test_size]
test = weekly.iloc[-test_size:]

model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=52,
    initialization_method="estimated"
).fit()

forecast = model.forecast(test_size)

result = pd.DataFrame({
    "Actual": test.values,
    "Forecast": forecast.values
}, index=test.index)

result["Absolute_Error"] = (result["Actual"] - result["Forecast"]).abs()
print(result)
print("\nMAE:", result["Absolute_Error"].mean())