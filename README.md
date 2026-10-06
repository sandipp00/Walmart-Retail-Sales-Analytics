# Walmart Retail Sales Analytics & Demand Forecasting

End-to-end retail analytics project combining **Python, SQL, Power BI, machine learning, and time-series forecasting** on Walmart weekly store sales.

## Dataset

- **6,435** weekly observations
- **45** stores
- **2010-02-05 to 2012-10-26**
- Store-level weekly sales and holiday/economic variables
- No missing values in the cleaned dataset

## Business Questions

- Which stores contribute the most sales?
- How does sales performance vary over time and around holidays?
- What relationships exist between sales and economic variables?
- How accurately can future weekly sales be forecast?
- Which forecasting approach performs best against simple baselines?

## Project Workflow

1. Data validation and cleaning
2. Feature engineering
3. Exploratory and business analysis
4. SQL analysis
5. Power BI dashboarding
6. Time-aware machine-learning prediction
7. Time-series model comparison
8. Streamlit analytics application

## Forecasting Methodology

The forecasting evaluation uses the final **12 weeks** as a chronological holdout set. No future observations are used when generating forecasts.

The time-series comparison includes:

| Model | Purpose |
|---|---|
| Naive | Last-value baseline |
| Moving Average (4) | Short-term smoothing baseline |
| Seasonal Naive (52) | Previous-year weekly seasonal baseline |
| Holt-Winters | Trend + annual seasonality |

Evaluation metrics:

- **MAE** — Mean Absolute Error
- **RMSE** — Root Mean Squared Error
- **MAPE** — Mean Absolute Percentage Error

Run the forecasting pipeline with:

```bash
python src/forecasting.py
```

It generates:

- `reports/forecast_model_comparison.csv`
- `reports/forecast_holdout_results.csv`

The script automatically ranks the forecasting approaches by MAE. After execution, the generated CSV files are available under `reports/`; model metrics are intentionally not hard-coded into the README.

### Machine-learning model

A separate time-aware **Random Forest Regressor** uses an 80/20 chronological split with store, holiday, weather, economic, and calendar features. Its evaluation is kept separate from the univariate time-series comparison because it uses additional explanatory variables.


## Dashboard

The Streamlit dashboard provides interactive store/year/holiday filters, sales KPIs, store rankings, seasonality analysis, and forecast evaluation.

- **Live app:** https://walmart-retail-sales-analytics-gnya4mgzakht7sxpkffv5d.streamlit.app/
- Store selection is optional; leaving it empty includes all stores.
- Forecast outputs are shown when the generated evaluation CSVs are present.

### Verified Forecast Results

The four-model comparison was executed against the repository dataset using a chronological 12-week holdout:

| Model | MAE | RMSE | MAPE |
|---|---:|---:|---:|
| Holt-Winters | 668,758.84 | 839,173.80 | 1.44% |
| Seasonal Naive (52) | 974,641.62 | 1,160,987.12 | 2.12% |
| Moving Average (4) | 1,378,075.16 | 1,512,787.36 | 2.98% |
| Naive | 1,442,375.23 | 1,969,608.58 | 3.22% |

**Best model by MAE: Holt-Winters.**

The dashboard was also manually verified after the final UI refinement, including the optional Store filter and Holiday Avg Uplift KPI.

## Tech Stack

**Python:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Statsmodels  
**SQL:** MySQL, analytical queries, window functions, business-question queries  
**BI:** Power BI, DAX  
**App:** Streamlit, Plotly  
**Modeling:** Random Forest, Holt-Winters, forecasting baselines

## Run Locally

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Run the data pipeline:

```bash
python src/data_cleaning.py
python src/analysis.py
python src/forecasting.py
python src/train_model.py
```

Launch the Streamlit application:

```bash
streamlit run app/app.py
```

## Repository Structure

```text
Walmart-Retail-Sales-Analytics/
├── app/
│   └── app.py
├── dashboard/
│   ├── DAX_MEASURES.md
│   └── POWER_BI_GUIDE.md
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── reports/
│   ├── business_insights.md
│   ├── PROJECT_CHECKLIST.md
│   ├── forecast_model_comparison.csv
│   └── forecast_holdout_results.csv
├── sql/
└── src/
    ├── analysis.py
    ├── data_cleaning.py
    ├── feature_engineering.py
    ├── forecasting.py
    └── train_model.py
```

## Portfolio Project

**Walmart Retail Sales Analytics & Demand Forecasting | Python, SQL, Power BI, Machine Learning**

Built an end-to-end retail analytics solution using 6,435 Walmart weekly sales records across 45 stores, combining business analysis, SQL, Power BI, machine-learning prediction, and time-series forecasting with reproducible model evaluation.
