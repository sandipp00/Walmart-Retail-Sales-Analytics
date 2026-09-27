from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "walmart_cleaned.csv"

st.set_page_config(page_title="Walmart Sales Analytics", layout="wide")
st.title("Walmart Retail Sales Analytics")

df = pd.read_csv(DATA, parse_dates=["Date"])

stores = st.sidebar.multiselect(
    "Store",
    sorted(df["Store"].unique()),
    default=sorted(df["Store"].unique())
)
year = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

filtered = df[df["Store"].isin(stores) & df["Year"].isin(year)]

c1, c2, c3 = st.columns(3)
c1.metric("Total Sales", f"${filtered['Weekly_Sales'].sum():,.0f}")
c2.metric("Avg Weekly Sales", f"${filtered['Weekly_Sales'].mean():,.0f}")
c3.metric("Stores", f"{filtered['Store'].nunique()}")

trend = filtered.groupby("Date", as_index=False)["Weekly_Sales"].sum()
fig = px.line(trend, x="Date", y="Weekly_Sales", title="Weekly Sales Trend")
st.plotly_chart(fig, use_container_width=True)

store_sales = (
    filtered.groupby("Store", as_index=False)["Weekly_Sales"]
    .sum()
    .sort_values("Weekly_Sales", ascending=False)
)
fig2 = px.bar(
    store_sales,
    x="Store",
    y="Weekly_Sales",
    title="Sales by Store"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Holiday Comparison")
holiday = filtered.groupby("Holiday", as_index=False)["Weekly_Sales"].mean()
fig3 = px.bar(holiday, x="Holiday", y="Weekly_Sales", title="Average Sales: Holiday vs Non-Holiday")
st.plotly_chart(fig3, use_container_width=True)
