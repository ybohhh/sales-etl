# AWS Serverless Sales ETL Pipeline

**One-line:** Event-driven serverless ETL that validates, cleans and aggregates e-commerce sales CSVs using S3 → Lambda → RDS (Postgres), with CloudWatch monitoring & SNS alerts.  
Demo-ready for interviews.

---

## Repository contents
- `lambda/` — Lambda handler & requirements (ETL logic)
- `generate_sales_data.py` — synthetic sales generator (for local testing)
- `dashboard.py` — small Flask dashboard (local demo)
- `templates/index.html` — dashboard HTML
- `schema.sql` — database schema (create required tables)
- `screenshots/` — recommended screenshots for portfolio (add PNGs here)
- `.gitignore`, `LICENSE`

---

## Quick demo (what I will show in interviews)
1. Upload CSV → S3 triggers Lambda (show CloudWatch logs).  
2. Lambda writes cleaned data + metrics to RDS → show SQL results.  
3. CloudWatch custom metrics & SNS email alert demo.  
4. Local Flask dashboard reads metrics and shows trends.

---

## How to run the dashboard locally (for reviewers)

**Prereqs**
- Python 3.11/3.13
- `psql` client (optional)
- Access to the RDS instance (security group must allow your IP)
- AWS CLI configured (optional for S3 uploads)

**1. Create venv & install**
```bash
cd /path/to/sales-etl
python3 -m venv venv
source venv/bin/activate
pip install -r lambda/requirements.txt    # install deps used in Lambda if needed
pip install flask psycopg2-binary
