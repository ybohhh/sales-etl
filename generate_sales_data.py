import csv
import random
from datetime import datetime, timedelta
import uuid

def generate_sales_data(num_records=10000):
    """Generate realistic sales transaction data"""
    
    products = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Monitor', 
                'Keyboard', 'Mouse', 'Webcam', 'Speaker', 'Charger']
    
    categories = ['Electronics', 'Accessories', 'Computers']
    
    regions = ['East', 'West', 'North', 'South', 'Central']
    
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Cash']
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        transaction_id = str(uuid.uuid4())
        
        # Some intentional data quality issues
        if random.random() < 0.05:  # 5% bad data
            product = None  # Missing product
            quantity = -1   # Invalid quantity
            price = "invalid"  # Bad price format
        else:
            product = random.choice(products)
            quantity = random.randint(1, 10)
            price = round(random.uniform(10, 2000), 2)
        
        customer_id = f"CUST{random.randint(1000, 9999)}"
        region = random.choice(regions)
        payment = random.choice(payment_methods)
        
        # Random date within 2024
        days_offset = random.randint(0, 300)
        transaction_date = start_date + timedelta(days=days_offset)
        
        data.append({
            'transaction_id': transaction_id,
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'customer_id': customer_id,
            'product': product,
            'quantity': quantity,
            'price': price,
            'region': region,
            'payment_method': payment
        })
    
    return data

def save_to_csv(data, filename='sales_data.csv'):
    """Save data to CSV file"""
    fieldnames = ['transaction_id', 'transaction_date', 'customer_id', 
                  'product', 'quantity', 'price', 'region', 'payment_method']
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Generated {len(data)} records in {filename}")

if __name__ == "__main__":
    sales_data = generate_sales_data(10000)
    save_to_csv(sales_data, 'sales_data_2024_11_10.csv')
