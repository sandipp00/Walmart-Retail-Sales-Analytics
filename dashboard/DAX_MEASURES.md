# Recommended DAX Measures

```DAX
Total Sales = SUM(Walmart[Weekly_Sales])

Average Weekly Sales = AVERAGE(Walmart[Weekly_Sales])

Total Stores = DISTINCTCOUNT(Walmart[Store])

Holiday Sales = CALCULATE([Total Sales], Walmart[Holiday_Flag] = 1)

Non Holiday Sales = CALCULATE([Total Sales], Walmart[Holiday_Flag] = 0)

Sales YoY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Calendar'[Date]))

YoY Growth % = DIVIDE([Total Sales] - [Sales YoY], [Sales YoY])

Sales per Store = DIVIDE([Total Sales], [Total Stores])
```

## Recommended Calendar Table

Create a dedicated calendar table and mark it as the model's date table:

```DAX
Calendar =
ADDCOLUMNS(
    CALENDAR(MIN(Walmart[Date]), MAX(Walmart[Date])),
    "Year", YEAR([Date]),
    "Month Number", MONTH([Date]),
    "Month", FORMAT([Date], "MMMM"),
    "Quarter", "Q" & FORMAT([Date], "Q")
)
```

Relate `Calendar[Date]` (1) to `Walmart[Date]` (*).

## KPI Interpretation

- **Total Sales:** aggregate sales for the selected period/stores.
- **Average Weekly Sales:** average observation-level weekly sales.
- **Holiday Sales / Non Holiday Sales:** total sales restricted by holiday flag.
- **YoY Growth %:** year-over-year change using the Calendar table.
- **Sales per Store:** total sales divided by the number of stores in the current filter context.