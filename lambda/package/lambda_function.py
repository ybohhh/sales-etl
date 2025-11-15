# lambda_function.py
import json, os, csv
from io import StringIO
from datetime import datetime
import boto3
import psycopg2
from psycopg2.extras import execute_values

s3 = boto3.client('s3')
cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME', 'salesdb')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def publish_metrics(valid_count, invalid_count, quality_rate):
    try:
        cloudwatch.put_metric_data(
            Namespace='SalesETL',
            MetricData=[
                {'MetricName':'RecordsProcessed','Value':valid_count,'Unit':'Count','Timestamp':datetime.utcnow()},
                {'MetricName':'InvalidRecords','Value':invalid_count,'Unit':'Count','Timestamp':datetime.utcnow()},
                {'MetricName':'DataQualityRate','Value':quality_rate,'Unit':'Percent','Timestamp':datetime.utcnow()}
            ]
        )
    except Exception as e:
        print("Failed to publish metrics:", e)

def send_alert(subject, message):
    if not SNS_TOPIC_ARN:
        print("SNS_TOPIC_ARN not set, skipping alert")
        return
    try:
        sns.publish(TopicArn=SNS_TOPIC_ARN, Subject=subject, Message=message)
    except Exception as e:
        print("Failed to publish SNS:", e)

def parse_csv(content):
    rows = list(csv.DictReader(StringIO(content)))
    return rows

def validate_record(r):
    errors = []
    if not r.get('product') or r.get('product') in ('', 'None'):
        errors.append('missing_product')
    try:
        q = int(r.get('quantity', 0))
        if q <= 0:
            errors.append('invalid_quantity')
    except:
        errors.append('quantity_not_int')
    try:
        p = float(r.get('price'))
        if p <= 0:
            errors.append('invalid_price')
    except:
        errors.append('price_not_float')
    return errors

def lambda_handler(event, context):
    conn = None
    cursor = None
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(f"Start processing s3://{bucket}/{key}")
        resp = s3.get_object(Bucket=bucket, Key=key)
        content = resp['Body'].read().decode('utf-8')
        rows = parse_csv(content)
        total = len(rows)
        valid_rows = []
        invalid_rows = []
        error_types = []

        for r in rows:
            errs = validate_record(r)
            if errs:
                invalid_rows.append(r)
                error_types.extend(errs)
            else:
                q = int(r['quantity'])
                p = float(r['price'])
                total_amount = round(q * p, 2)
                valid_rows.append((
                    r['transaction_id'],
                    r['transaction_date'],
                    r['customer_id'],
                    r['product'],
                    q,
                    p,
                    total_amount,
                    r.get('region'),
                    r.get('payment_method')
                ))

        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()

        if valid_rows:
            insert_sql = """
                INSERT INTO sales_transactions_clean
                (transaction_id, transaction_date, customer_id, product, quantity, price, total_amount, region, payment_method)
                VALUES %s
                ON CONFLICT (transaction_id) DO NOTHING
            """
            execute_values(cursor, insert_sql, valid_rows, page_size=1000)
            print(f"Inserted {len(valid_rows)} rows")

        cursor.execute("""
            INSERT INTO daily_metrics
            (metric_date, total_transactions, total_revenue, avg_transaction_value, total_quantity, unique_customers)
            SELECT transaction_date,
                   COUNT(*) as total_transactions,
                   SUM(total_amount) as total_revenue,
                   AVG(total_amount) as avg_transaction_value,
                   SUM(quantity) as total_quantity,
                   COUNT(DISTINCT customer_id) as unique_customers
            FROM sales_transactions_clean
            GROUP BY transaction_date
            ON CONFLICT (metric_date)
            DO UPDATE SET
                total_transactions = EXCLUDED.total_transactions,
                total_revenue = EXCLUDED.total_revenue,
                avg_transaction_value = EXCLUDED.avg_transaction_value,
                total_quantity = EXCLUDED.total_quantity,
                unique_customers = EXCLUDED.unique_customers,
                calculated_at = CURRENT_TIMESTAMP
        """)
        cursor.execute("""
            INSERT INTO data_quality_log (file_name, total_records, valid_records, invalid_records, error_types)
            VALUES (%s, %s, %s, %s, %s)
        """, (key, total, len(valid_rows), len(invalid_rows), ','.join(list(set(error_types)))))

        conn.commit()

        if valid_rows:
            processed_csv = StringIO()
            writer = csv.writer(processed_csv)
            writer.writerow(['transaction_id','transaction_date','customer_id','product','quantity','price','total_amount','region','payment_method'])
            writer.writerows(valid_rows)
            processed_key = key.rsplit('.',1)[0] + '_processed.csv'
            processed_bucket = bucket.replace('raw', 'processed')
            try:
                s3.put_object(Bucket=processed_bucket, Key=processed_key, Body=processed_csv.getvalue())
            except Exception as e:
                print("Failed to upload processed file:", e)

        valid_count = len(valid_rows)
        invalid_count = len(invalid_rows)
        quality_rate = round((valid_count / total * 100) if total>0 else 0, 2)
        publish_metrics(valid_count, invalid_count, quality_rate)

        if quality_rate < 90:
            send_alert('⚠️ Sales ETL Data Quality Alert',
                       f'File: {key}\nTotal: {total}\nValid: {valid_count}\nInvalid: {invalid_count}\nQuality: {quality_rate}%\nErrors: {list(set(error_types))}')

        return {
            'statusCode': 200,
            'body': json.dumps({'message':'OK','file': key, 'total': total, 'valid': valid_count, 'invalid': invalid_count})
        }

    except Exception as e:
        print("Lambda error:", e)
        return {'statusCode':500,'body':json.dumps({'error': str(e)})}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

