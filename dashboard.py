# dashboard.py
from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    # 添加调试信息
    print(f"Connecting to: host={os.environ.get('DB_HOST')}, database={os.environ.get('DB_NAME')}, user={os.environ.get('DB_USER')}")
    
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD')
    )
    
    # 测试连接并检查表是否存在
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name = 'daily_metrics'
    """)
    table_exists = cursor.fetchone()
    print(f"Table 'daily_metrics' exists: {table_exists}")
    cursor.close()
    
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 先执行一个简单的查询测试
        cursor.execute("SELECT COUNT(*) FROM daily_metrics")
        count = cursor.fetchone()
        print(f"Records in daily_metrics: {count}")
        
        # 然后执行您的实际查询
        cursor.execute("""
            SELECT 
                SUM(total_transactions) as transactions,
                SUM(total_revenue) as revenue,
                AVG(avg_transaction_value) as avg_value,
                SUM(unique_customers) as customers
            FROM daily_metrics
            WHERE metric_date >= CURRENT_DATE - INTERVAL '7 days'
        """)
        stats = cursor.fetchone()
        
        # 其余代码保持不变...
        cursor.execute("""
            SELECT file_name, total_records, valid_records, invalid_records,
                   ROUND((valid_records::numeric / total_records * 100), 2) as quality_rate,
                   processed_at
            FROM data_quality_log
            ORDER BY processed_at DESC
            LIMIT 10
        """)
        quality_logs = cursor.fetchall()
        
        cursor.execute("""
            SELECT metric_date, total_transactions, total_revenue
            FROM daily_metrics
            ORDER BY metric_date DESC
            LIMIT 30
        """)
        trends = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return render_template('index.html', stats=stats, quality_logs=quality_logs, trends=trends)
    
    except Exception as e:
        print(f"Error: {e}")
        return f"Database error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
