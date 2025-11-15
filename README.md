# AWS Serverless Sales ETL Pipeline

**One-line:** Event-driven serverless ETL that validates, cleans and aggregates e-commerce sales CSVs using S3 → Lambda → RDS (Postgres), with CloudWatch monitoring & SNS alerts. Demo-ready for interviews.

---

## Project summary (what & why)
An e-commerce pipeline that:
- Automatically processes uploaded sales CSVs in S3.
- Cleans and validates rows (nulls, negative quantities, price format).
- Stores cleaned rows in Postgres and calculates daily metrics for BI.
- Emits custom CloudWatch metrics and sends SNS alerts on low data quality.
- Includes a small Flask dashboard for stakeholder demo.

**Skills demonstrated:** AWS (Lambda, S3, RDS, CloudWatch, SNS), Python (boto3, psycopg2), SQL, data validation, monitoring, small web dashboard.

---

## Repo contents (important files)
- `lambda/` — Lambda handler and `requirements.txt` used for packaging
- `dashboard/` or `dashboard.py` — Flask demo (local)
- `templates/index.html` — dashboard HTML
- `generate_sales_data.py` — synthetic data generator
- `schema.sql` — database schema (DDL) — **run this to create tables**
- `requirements.txt` — Python dependencies for local/dev
- `architecture.png` — architecture diagram
- `screenshots/` — recommended screenshots for README
- `run_local.sh` — helper script to run local demo (see below)
- `.env.example` — example env file (do **not** commit secrets)

---

## Quick demo (2 minutes to show in interview)
1. Show architecture.png and explain flow (S3 → Lambda → RDS → Dashboard).
2. Upload `data/sample_sales.csv` to S3 raw bucket (or run local generate script).
3. Show Lambda CloudWatch logs (function invoked).
4. Show `SELECT * FROM daily_metrics` in RDS (psql) and Flask dashboard at `http://localhost:5000`.
5. Trigger a bad-data upload to show SNS email alert.

---

## How to run locally (developer / reviewer)
**Prereqs**
- Python 3.11+ (3.13 OK)
- `psql` client (optional)
- AWS CLI configured (if you will upload to S3)
- Network access to your RDS instance (Security Group must allow your IP)

**1. Create virtualenv and install deps**
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install flask psycopg2-binary
