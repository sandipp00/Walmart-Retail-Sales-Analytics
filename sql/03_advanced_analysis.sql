USE walmart_analytics;

WITH store_sales AS (
    SELECT Store, SUM(Weekly_Sales) AS Total_Sales
    FROM walmart_sales
    GROUP BY Store
)
SELECT Store,
       ROUND(Total_Sales, 2) AS Total_Sales,
       DENSE_RANK() OVER (ORDER BY Total_Sales DESC) AS Sales_Rank
FROM store_sales
ORDER BY Sales_Rank;

WITH monthly AS (
    SELECT DATE_FORMAT(Date, '%Y-%m') AS Year_Month,
           SUM(Weekly_Sales) AS Sales
    FROM walmart_sales
    GROUP BY DATE_FORMAT(Date, '%Y-%m')
)
SELECT Year_Month,
       ROUND(Sales, 2) AS Sales,
       ROUND(
           (Sales - LAG(Sales) OVER (ORDER BY Year_Month))
           / NULLIF(LAG(Sales) OVER (ORDER BY Year_Month), 0) * 100, 2
       ) AS MoM_Growth_Pct
FROM monthly
ORDER BY Year_Month;