# Recommended DAX Measures

Total Sales = SUM(Walmart[Weekly_Sales])

Average Weekly Sales = AVERAGE(Walmart[Weekly_Sales])

Total Stores = DISTINCTCOUNT(Walmart[Store])

Holiday Sales = CALCULATE([Total Sales], Walmart[Holiday_Flag] = 1)

Non Holiday Sales = CALCULATE([Total Sales], Walmart[Holiday_Flag] = 0)

Sales YoY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Calendar'[Date]))

YoY Growth % = DIVIDE([Total Sales] - [Sales YoY], [Sales YoY])

Sales per Store = DIVIDE([Total Sales], [Total Stores])