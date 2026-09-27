import pandas as pd

def add_time_features(df):
    df = df.copy()
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Quarter"] = df["Date"].dt.quarter
    df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
    df["Days_Since_Start"] = (df["Date"] - df["Date"].min()).dt.days
    return df

def build_model_data(df):
    df = add_time_features(df)
    features = [
        "Store", "Holiday_Flag", "Temperature", "Fuel_Price",
        "CPI", "Unemployment", "Year", "Month", "Quarter",
        "Week", "Days_Since_Start"
    ]
    return df[features + ["Weekly_Sales"]].dropna()