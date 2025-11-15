schema.sql
Create tables for Sales ETL pipeline demo
CREATE TABLE IF NOT EXISTS sales_transactions_raw (
    transaction_id VARCHAR(100) PRIMARY KEY,
    transaction_date DATE,
    customer_id VARCHAR(50),
    product VARCHAR(100),
    quantity INTEGER,
    price DECIMAL(10,2),
    region VARCHAR(50),
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales_transactions_clean (
    transaction_id VARCHAR(100) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    product VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    total_amount DECIMAL(14, 2),
    region VARCHAR(50),
    payment_method VARCHAR(50),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS daily_metrics (
    metric_date DATE PRIMARY KEY,
    total_transactions INTEGER,
    total_revenue DECIMAL(16,2),
    avg_transaction_value DECIMAL(12,2),
    total_quantity INTEGER,
    unique_customers INTEGER,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_quality_log (
    log_id SERIAL PRIMARY KEY,
    file_name VARCHAR(255),
    total_records INTEGER,
    valid_records INTEGER,
    invalid_records INTEGER,
    error_types TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
