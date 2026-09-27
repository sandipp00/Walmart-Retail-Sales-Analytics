from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "walmart_cleaned.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Quarter"] = df["Date"].dt.quarter
df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
df["Days_Since_Start"] = (df["Date"] - df["Date"].min()).dt.days

features = ["Store", "Holiday_Flag", "Temperature", "Fuel_Price", "CPI",
            "Unemployment", "Year", "Month", "Quarter", "Week", "Days_Since_Start"]

df = df.sort_values("Date")
cutoff = df["Date"].quantile(0.80)
train = df[df["Date"] <= cutoff]
test = df[df["Date"] > cutoff]

X_train, y_train = train[features], train["Weekly_Sales"]
X_test, y_test = test[features], test["Weekly_Sales"]

model = RandomForestRegressor(
    n_estimators=300, random_state=42, n_jobs=-1, max_features="sqrt"
)
model.fit(X_train, y_train)
pred = model.predict(X_test)

mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)

print(f"MAE : {mae:,.2f}")
print(f"RMSE: {rmse:,.2f}")
print(f"R2  : {r2:.4f}")

joblib.dump(model, MODEL_DIR / "sales_random_forest.pkl")