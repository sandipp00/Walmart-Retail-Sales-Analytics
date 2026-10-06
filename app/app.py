from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "walmart_cleaned.csv"
FORECAST_METRICS = ROOT / "reports" / "forecast_model_comparison.csv"
FORECAST_HOLDOUT = ROOT / "reports" / "forecast_holdout_results.csv"

st.set_page_config(page_title="Walmart Sales Analytics", page_icon="📊", layout="wide")
st.title("Walmart Retail Sales Analytics")
st.caption("Interactive sales performance, seasonality, holiday impact, and forecasting analysis.")

df = pd.read_csv(DATA, parse_dates=["Date"])

with st.sidebar:
    st.header("Filters")
    stores = st.multiselect("Store", sorted(df["Store"].unique()), default=sorted(df["Store"].unique()))
    years = st.multiselect("Year", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
    holidays = st.multiselect("Holiday", sorted(df["Holiday"].unique()), default=sorted(df["Holiday"].unique()))

filtered = df[df["Store"].isin(stores) & df["Year"].isin(years) & df["Holiday"].isin(holidays)].copy()

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

total_sales = filtered["Weekly_Sales"].sum()
avg_weekly = filtered["Weekly_Sales"].mean()
store_count = filtered["Store"].nunique()
holiday_share = (filtered.loc[filtered["Holiday_Flag"] == 1, "Weekly_Sales"].sum() / total_sales * 100) if total_sales else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${total_sales:,.0f}")
c2.metric("Avg Weekly Sales", f"${avg_weekly:,.0f}")
c3.metric("Stores", f"{store_count}")
c4.metric("Holiday Sales Share", f"{holiday_share:.1f}%")

st.divider()

left, right = st.columns(2)
with left:
    trend = filtered.groupby("Date", as_index=False)["Weekly_Sales"].sum()
    fig = px.line(trend, x="Date", y="Weekly_Sales", title="Weekly Sales Trend")
    st.plotly_chart(fig, use_container_width=True)
with right:
    store_sales = filtered.groupby("Store", as_index=False)["Weekly_Sales"].sum().sort_values("Weekly_Sales", ascending=False)
    fig2 = px.bar(store_sales, x="Store", y="Weekly_Sales", title="Sales by Store")
    st.plotly_chart(fig2, use_container_width=True)

left, right = st.columns(2)
with left:
    holiday = filtered.groupby("Holiday", as_index=False)["Weekly_Sales"].mean()
    fig3 = px.bar(holiday, x="Holiday", y="Weekly_Sales", title="Average Sales: Holiday vs Non-Holiday")
    st.plotly_chart(fig3, use_container_width=True)
with right:
    monthly = filtered.groupby("Month_Name", as_index=False)["Weekly_Sales"].mean()
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    monthly["Month_Name"] = pd.Categorical(monthly["Month_Name"], categories=month_order, ordered=True)
    monthly = monthly.sort_values("Month_Name")
    fig4 = px.bar(monthly, x="Month_Name", y="Weekly_Sales", title="Average Sales by Month")
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Top and Bottom Stores")
ranking = filtered.groupby("Store", as_index=False)["Weekly_Sales"].agg(Total_Sales="sum", Avg_Weekly_Sales="mean").sort_values("Total_Sales", ascending=False)
top, bottom = st.columns(2)
with top:
    st.dataframe(ranking.head(5), hide_index=True, use_container_width=True)
with bottom:
    st.dataframe(ranking.tail(5).sort_values("Total_Sales"), hide_index=True, use_container_width=True)

st.subheader("Forecast Model Comparison")
if FORECAST_METRICS.exists():
    metrics = pd.read_csv(FORECAST_METRICS)
    st.dataframe(metrics, hide_index=True, use_container_width=True)
    if FORECAST_HOLDOUT.exists():
        holdout = pd.read_csv(FORECAST_HOLDOUT, parse_dates=["Date"])
        fig5 = px.line(holdout, x="Date", y=["Actual", "Forecast"], title="Holdout Forecast vs Actual Sales", markers=True)
        st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Run `python src/forecasting.py` to generate model-comparison and holdout forecast outputs.")