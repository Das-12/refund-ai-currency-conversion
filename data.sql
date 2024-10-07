CREATE TABLE currency_conversion_rates (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    base_currency TEXT NOT NULL,
    target_currency TEXT NOT NULL,
    conversion_rate REAL NOT NULL,
    timestamp DATETIME NOT NULL
);