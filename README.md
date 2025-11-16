# 📦 Sales Analytics ETL Pipeline (AWS Lambda + S3 + Postgres + Flask Dashboard)

A production-ready, event-driven ETL pipeline that simulates real sales data, lands it in AWS S3, transforms it through AWS Lambda, loads results into PostgreSQL (Amazon RDS), and visualizes business metrics in a custom Flask dashboard.

This project is designed for Data Engineering / Analytics Engineering / Data Analyst / Data Science roles — demonstrating your ability to work with pipelines, cloud services, databases, and dashboards end-to-end.

## 🚀 Features

✔ **1. Automated Data Generation**
- Synthetic sales events created daily using Python
- CSV files structured for real analytics scenarios
- Parameterized: product mix, regional distribution, revenue ranges

✔ **2. Cloud ETL Pipeline (Serverless)**
- Data uploaded to AWS S3
- AWS Lambda automatically triggered on file arrival
- Cleans, validates, aggregates, and loads metrics into PostgreSQL (RDS)

✔ **3. Analytical Data Model**
- Fact-style daily_metrics table including:
  - total revenue
  - total units sold
  - unique customers
  - top-performing products
  - transaction count

✔ **4. Interactive Analytics Dashboard**
- Flask web app reading directly from Postgres
- Clean UI
- Daily trend visualizations + KPI summary

✔ **5. Production-Ready Repository**
- requirements.txt
- lambda/package build instructions
- .gitignore
- Visual architecture + screenshots

## 🏗 Architecture

Below is the full architecture of this project:

![Architecture Diagram](architecture.png)

## 📊 Dashboard Preview

![Dashboard Screenshot](dashboard_screenshot.png)

## 📁 Repository Structure

## 📚 Data Model

**Table: daily_metrics**

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Sales date |
| total_revenue | NUMERIC | Total daily revenue |
| total_units_sold | INT | Total quantity sold |
| unique_customers | INT | Number of distinct buyers |
| order_count | INT | Number of transactions |
| top_product | TEXT | Best-selling product |
| created_at | TIMESTAMP | ETL load timestamp |

## 🔄 ETL Flow

1. Generate CSV using `generate_sales_data.py`
2. CSV uploaded to S3 bucket
3. S3 triggers AWS Lambda
4. Lambda parses CSV, validates data, computes metrics
5. Lambda inserts aggregated metrics into PostgreSQL RDS
6. Flask dashboard queries RDS to render daily insights

## ▶ How to Run Locally (Dashboard)

### 1️⃣ Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
