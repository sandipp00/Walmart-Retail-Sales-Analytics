from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "walmart_cleaned.csv"
REPORT = ROOT / "reports"
REPORT.mkdir(exist_ok=True)

TEST_SIZE = 12
SEASONAL_PERIODS = 52


def mean_absolute_percentage_error(actual, predicted):
    """Return MAPE as a percentage, ignoring zero actual values."""
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    mask = actual != 0
    if not mask.any():
        return np.nan
    return np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100


def evaluate_forecast(actual, predicted):
    """Calculate MAE, RMSE and MAPE for a forecast."""
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    error = actual - predicted
    return {
        "MAE": np.mean(np.abs(error)),
        "RMSE": np.sqrt(np.mean(error ** 2)),
        "MAPE": mean_absolute_percentage_error(actual, predicted),
    }


def naive_forecast(train, horizon):
    return np.repeat(train.iloc[-1], horizon)


def moving_average_forecast(train, horizon, window=4):
    return np.repeat(train.iloc[-window:].mean(), horizon)


def seasonal_naive_forecast(train, horizon, seasonal_periods=52):
    if len(train) < seasonal_periods:
        raise ValueError(
            f"Need at least {seasonal_periods} training observations "
            "for seasonal naive forecasting."
        )
    last_season = train.iloc[-seasonal_periods:].to_numpy()
    repeats = int(np.ceil(horizon / seasonal_periods))
    return np.tile(last_season, repeats)[:horizon]


def holt_winters_forecast(train, horizon, seasonal_periods=52):
    model = ExponentialSmoothing(
        train,
        trend="add",
        seasonal="add",
        seasonal_periods=seasonal_periods,
        initialization_method="estimated",
    ).fit()
    return model.forecast(horizon).to_numpy()


def build_weekly_series(df):
    """Aggregate store-level observations into a regular weekly series."""
    weekly = df.groupby("Date")["Weekly_Sales"].sum().sort_index()
    weekly = weekly.asfreq("7D")
    if weekly.isna().any():
        raise ValueError("Weekly sales series contains missing dates/values.")
    return weekly


def compare_models(weekly, test_size=TEST_SIZE):
    """Compare time-series baselines and Holt-Winters on a final holdout."""
    if len(weekly) <= test_size + SEASONAL_PERIODS:
        raise ValueError("Not enough observations for the selected test window.")

    train = weekly.iloc[:-test_size]
    test = weekly.iloc[-test_size:]

    predictions = {
        "Naive": naive_forecast(train, test_size),
        "Moving Average (4)": moving_average_forecast(train, test_size, window=4),
        "Seasonal Naive (52)": seasonal_naive_forecast(
            train, test_size, seasonal_periods=SEASONAL_PERIODS
        ),
        "Holt-Winters": holt_winters_forecast(
            train, test_size, seasonal_periods=SEASONAL_PERIODS
        ),
    }

    rows = []
    for model_name, prediction in predictions.items():
        rows.append(
            {"Model": model_name, **evaluate_forecast(test.to_numpy(), prediction)}
        )

    metrics_df = pd.DataFrame(rows).sort_values("MAE").reset_index(drop=True)
    best_model = metrics_df.iloc[0]["Model"]
    best_prediction = predictions[best_model]

    forecast_result = pd.DataFrame(
        {
            "Date": test.index,
            "Actual": test.to_numpy(),
            "Forecast": best_prediction,
            "Absolute_Error": np.abs(test.to_numpy() - best_prediction),
        }
    )

    return metrics_df, forecast_result


def main():
    df = pd.read_csv(DATA, parse_dates=["Date"])
    weekly = build_weekly_series(df)
    metrics_df, forecast_result = compare_models(weekly)

    metrics_path = REPORT / "forecast_model_comparison.csv"
    forecast_path = REPORT / "forecast_holdout_results.csv"

    metrics_df.to_csv(metrics_path, index=False)
    forecast_result.to_csv(forecast_path, index=False)

    print("\nForecast model comparison")
    print(metrics_df.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    print(f"\nBest model by MAE: {metrics_df.iloc[0]['Model']}")
    print(f"Saved metrics to: {metrics_path}")
    print(f"Saved holdout predictions to: {forecast_path}")


if __name__ == "__main__":
    main()
