USE walmart_analytics;

SELECT Store, SUM(Weekly_Sales) AS Total_Sales
FROM walmart_sales
GROUP BY Store
ORDER BY Total_Sales DESC
LIMIT 1;

SELECT Store, SUM(Weekly_Sales) AS Total_Sales
FROM walmart_sales
GROUP BY Store
ORDER BY Total_Sales ASC
LIMIT 1;

SELECT Store, AVG(Weekly_Sales) AS Avg_Weekly_Sales
FROM walmart_sales
GROUP BY Store
ORDER BY Avg_Weekly_Sales DESC
LIMIT 1;

SELECT Store, Date, Weekly_Sales
FROM walmart_sales
ORDER BY Weekly_Sales DESC
LIMIT 10;

SELECT MONTH(Date) AS Month_Number,
       MONTHNAME(Date) AS Month_Name,
       SUM(Weekly_Sales) AS Sales
FROM walmart_sales
GROUP BY MONTH(Date), MONTHNAME(Date)
ORDER BY Month_Number;

SELECT Holiday_Flag, AVG(Weekly_Sales) AS Avg_Sales
FROM walmart_sales
GROUP BY Holiday_Flag;