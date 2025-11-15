sample_queries.sql
-- 1) Show last 7 days KPIs
SELECT metric_date, total_transactions, total_revenue, avg_transaction_value
FROM daily_metrics
ORDER BY metric_date DESC
LIMIT 7;

-- 2) Data quality recent
SELECT * FROM data_quality_log ORDER BY processed_at DESC LIMIT 10;
