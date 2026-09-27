USE walmart_analytics;

SELECT ROUND(SUM(Weekly_Sales), 2) AS Total_Sales
FROM walmart_sales;

SELECT Store, ROUND(SUM(Weekly_Sales), 2) AS Total_Sales
FROM walmart_sales
GROUP BY Store
ORDER BY Total_Sales DESC
LIMIT 10;

SELECT Store, ROUND(AVG(Weekly_Sales), 2) AS Avg_Weekly_Sales
FROM walmart_sales
GROUP BY Store
ORDER BY Avg_Weekly_Sales DESC;

SELECT Holiday_Flag,
       COUNT(*) AS Weeks,
       ROUND(AVG(Weekly_Sales), 2) AS Avg_Sales,
       ROUND(SUM(Weekly_Sales), 2) AS Total_Sales
FROM walmart_sales
GROUP BY Holiday_Flag;

SELECT YEAR(Date) AS Sales_Year,
       ROUND(SUM(Weekly_Sales), 2) AS Total_Sales
FROM walmart_sales
GROUP BY YEAR(Date)
ORDER BY Sales_Year;