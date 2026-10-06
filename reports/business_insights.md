# Business Insights

## Dataset profile

- **6,435** store-week observations
- **45** stores
- **2010-02-05 to 2012-10-26**
- Cleaned dataset contains no missing values
- Each store has regular weekly observations

## Store performance

Store-level aggregation shows a substantial difference between the highest- and lowest-performing stores. **Store 20** is the top store by cumulative weekly sales in the current analysis, while **Store 33** is the lowest.

### Business implication

Store performance should be evaluated separately from network-wide totals. High-volume stores can justify tighter inventory planning and higher replenishment priority, while lower-volume stores should be investigated for local demand, assortment, and operational differences before applying the same targets.

## Holiday analysis

Holiday-flagged weeks have higher average weekly sales than non-holiday weeks in the descriptive analysis:

- Holiday weeks: approximately **$1.123M** average weekly sales
- Non-holiday weeks: approximately **$1.041M**
- Observed difference: approximately **7.84%**

This is an **association, not a causal estimate**. Holiday weeks may coincide with other seasonal effects, so the result should not be interpreted as the incremental causal effect of a holiday.

### Business implication

Holiday periods should be incorporated into inventory and staffing planning. The forecasting workflow should also be evaluated carefully around holiday spikes because a model that performs well on ordinary weeks may underpredict peak demand.

## Forecasting strategy

The project now compares four approaches on a chronological 12-week holdout:

1. Naive
2. 4-week Moving Average
3. 52-week Seasonal Naive
4. Holt-Winters

The model comparison is generated programmatically by `src/forecasting.py` and saved to `reports/forecast_model_comparison.csv`.

### Business implication

The preferred forecasting model should be selected from **out-of-sample error**, not from model complexity. In particular, the seasonal-naive baseline is important because Walmart sales exhibit recurring annual patterns; Holt-Winters should only be preferred if it demonstrates measurable improvement over that baseline.

## Recommended actions

1. Use store-level sales rankings to prioritize inventory and operational reviews.
2. Build holiday-aware demand plans for peak weeks.
3. Compare forecast errors before selecting a production forecasting method.
4. Monitor forecast performance periodically rather than treating one holdout result as permanent.
5. Investigate store-specific drivers before using network-wide targets for every store.

> **Methodology note:** These findings are descriptive and should be combined with operational context before making business decisions. Forecast metrics should be generated from the repository pipeline rather than manually entered into this report.
