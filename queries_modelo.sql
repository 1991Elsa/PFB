CREATE DATABASE IF NOT EXISTS Yahoo_finance;

USE Yahoo_finance;

CREATE TABLE IF NOT EXISTS historic (
    Date DATE NOT NULL,
    Ticker VARCHAR(8) NOT NULL,
    Close FLOAT NOT NULL,
    High FLOAT NOT NULL,
    Low FLOAT NOT NULL,
    Open FLOAT NOT NULL,
    Volume BIGINT NOT NULL,
    PRIMARY KEY (Date, Ticker)
);

CREATE TABLE IF NOT EXISTS company_info (
    Ticker VARCHAR(8) PRIMARY KEY,
    ShortName VARCHAR(255) NOT NULL,
    Sector VARCHAR(255) NOT NULL,
    Industry VARCHAR(255) NOT NULL,
    Country VARCHAR(255) NOT NULL,
    FullTimeEmployees INT,
    MarketCap BIGINT,
    TotalRevenue BIGINT,
    NetIncomeToCommon BIGINT,
    TrailingEPS FLOAT,
    ForwardEPS FLOAT,  
    TrailingPE FLOAT,  
    ForwardPE FLOAT,   
    ReturnOnAssets FLOAT,
    ReturnOnEquity FLOAT,
    DebtToEquity FLOAT,
    FreeCashflow BIGINT,
    DividendRate FLOAT,
    DividendYield FLOAT,
    PayoutRatio FLOAT,
    Beta FLOAT,
    GrossMargins FLOAT,
    OperatingMargins FLOAT,
    ProfitMargins FLOAT,
    ebitdaMargins FLOAT,
    Timestamp_extraction TIMESTAMP 
);

SHOW TABLES;

DESCRIBE historic;
DESCRIBE company_info;
