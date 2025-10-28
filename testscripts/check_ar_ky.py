#!/usr/bin/env python3
"""Check ar_ky table schema and data"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=int(os.getenv('DB_PORT', '3306')),
    database='Thomas_More_University'
)

cursor = conn.cursor()

# Get schema
cursor.execute('DESCRIBE ar_ky')
cols = cursor.fetchall()

print('\nar_ky table schema:')
print('='*80)
print(f"{'Column':<40} {'Type':<20} {'Null'}")
print('-'*80)
for col in cols:
    print(f'{col[0]:<40} {col[1]:<20} {col[2]}')

# Get count
cursor.execute('SELECT COUNT(*) FROM ar_ky')
count = cursor.fetchone()[0]
print(f'\nTotal rows: {count}')

# Get sample row
if count > 0:
    cursor.execute('SELECT * FROM ar_ky LIMIT 1')
    row = cursor.fetchone()
    cursor.execute('DESCRIBE ar_ky')
    cols = cursor.fetchall()
    print('\nSample row (first record):')
    print('='*80)
    for i, col in enumerate(cols):
        print(f'{col[0]:<40} = {row[i]}')

cursor.close()
conn.close()
