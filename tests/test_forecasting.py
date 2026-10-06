import numpy as np
import pandas as pd

from src.forecasting import (
    evaluate_forecast,
    moving_average_forecast,
    naive_forecast,
    seasonal_naive_forecast,
)


def test_evaluate_forecast_metrics():
    actual = np.array([100.0, 200.0, 300.0])
    predicted = np.array([90.0, 210.0, 330.0])

    metrics = evaluate_forecast(actual, predicted)

    assert metrics["MAE"] == 16.666666666666666
    assert round(metrics["RMSE"], 6) == 17.320508
    assert round(metrics["MAPE"], 6) == 6.666667


def test_naive_forecast_repeats_last_value():
    train = pd.Series([10.0, 20.0, 30.0])
    prediction = naive_forecast(train, 4)
    assert prediction.tolist() == [30.0, 30.0, 30.0, 30.0]


def test_moving_average_forecast_uses_trailing_window():
    train = pd.Series([10.0, 20.0, 30.0, 40.0])
    prediction = moving_average_forecast(train, 2, window=2)
    assert prediction.tolist() == [35.0, 35.0]


def test_seasonal_naive_repeats_last_season():
    train = pd.Series(np.arange(1.0, 53.0))
    prediction = seasonal_naive_forecast(train, 5, seasonal_periods=52)
    assert prediction.tolist() == [1.0, 2.0, 3.0, 4.0, 5.0]
