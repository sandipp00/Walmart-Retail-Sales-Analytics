CREATE DATABASE IF NOT EXISTS walmart_analytics;
USE walmart_analytics;

CREATE TABLE walmart_sales (
    Store INT NOT NULL,
    Date DATE NOT NULL,
    Weekly_Sales DECIMAL(15,2) NOT NULL,
    Holiday_Flag TINYINT NOT NULL,
    Temperature DECIMAL(8,2),
    Fuel_Price DECIMAL(8,3),
    CPI DECIMAL(12,6),
    Unemployment DECIMAL(8,3),
    PRIMARY KEY (Store, Date)
);