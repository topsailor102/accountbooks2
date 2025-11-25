import pymysql
import time

DB_CONFIG = {
    'host': '192.168.178.36',
    'user': 'topsailor',
    'password': 'Wonyoung_470',
    'database': 'topsailor',
    'port': 3306,
}

print("Testing database connection...")
try:
    for i in range(3):
        print(f"Attempt {i+1}...")
        conn = pymysql.connect(**DB_CONFIG)
        print("Connected!")
        conn.close()
        time.sleep(1)
    print("All connection tests passed.")
except Exception as e:
    print(f"Connection failed: {e}")
