from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "walmart_cleaned.csv"

REQUIRED_COLUMNS = {
    "Store",
    "Date",
    "Weekly_Sales",
    "Holiday_Flag",
    "Temperature",
    "Fuel_Price",
    "CPI",
    "Unemployment",
    "Year",
    "Month",
    "Quarter",
    "Week",
    "Year_Month",
    "Holiday",
    "Sales_Million",
}


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA, parse_dates=["Date"])


def test_required_schema(df):
    assert REQUIRED_COLUMNS.issubset(df.columns)


def test_dataset_has_expected_store_count(df):
    assert df["Store"].nunique() == 45
    assert df["Store"].between(1, 45).all()


def test_core_fields_are_non_null(df):
    columns = [
        "Store",
        "Date",
        "Weekly_Sales",
        "Holiday_Flag",
        "Temperature",
        "Fuel_Price",
        "CPI",
        "Unemployment",
    ]
    assert df[columns].notna().all().all()


def test_sales_are_non_negative(df):
    assert (df["Weekly_Sales"] >= 0).all()
    assert np.isclose(df["Sales_Million"], df["Weekly_Sales"] / 1_000_000).all()


def test_holiday_values_are_valid(df):
    assert set(df["Holiday_Flag"].unique()).issubset({0, 1})
    assert set(df["Holiday"].unique()).issubset({"Holiday", "Non-Holiday"})


def test_store_dates_are_unique(df):
    assert not df.duplicated(["Store", "Date"]).any()


def test_each_store_has_regular_weekly_observations(df):
    gaps = (
        df.sort_values(["Store", "Date"])
        .groupby("Store")["Date"]
        .diff()
        .dropna()
    )
    assert (gaps == pd.Timedelta(days=7)).all()


def test_date_features_match_date_column(df):
    assert (df["Year"] == df["Date"].dt.year).all()
    assert (df["Month"] == df["Date"].dt.month).all()
    assert (df["Week"] == df["Date"].dt.isocalendar().week.astype(int)).all()
    assert (df["Year_Month"] == df["Date"].dt.to_period("M").astype(str)).all()
