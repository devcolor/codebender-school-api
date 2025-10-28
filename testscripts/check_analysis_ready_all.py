#!/usr/bin/env python3
"""Check analysis_ready_all table"""
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

# Get count
cursor.execute('SELECT COUNT(*) FROM analysis_ready_all')
count = cursor.fetchone()[0]
print(f'\nanalysis_ready_all total rows: {count}')

if count > 0:
    # Get schema
    cursor.execute('DESCRIBE analysis_ready_all')
    cols = cursor.fetchall()
    
    print('\nanalysis_ready_all table schema:')
    print('='*80)
    print(f"{'Column':<40} {'Type':<20} {'Null'}")
    print('-'*80)
    for col in cols:
        print(f'{col[0]:<40} {col[1]:<20} {col[2]}')
    
    # Get sample row
    cursor.execute('SELECT * FROM analysis_ready_all LIMIT 1')
    row = cursor.fetchone()
    print('\nSample row (first record):')
    print('='*80)
    for i, col in enumerate(cols):
        value = str(row[i])[:50] if row[i] is not None else 'NULL'
        print(f'{col[0]:<40} = {value}')

cursor.close()
conn.close()
