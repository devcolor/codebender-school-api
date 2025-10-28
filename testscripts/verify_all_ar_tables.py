#!/usr/bin/env python3
"""
Verify all ar_* tables have been populated
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'AL': ('Bishop_State_Community_College', 'ar_al'),
    'CSUSB': ('California_State_University_San_Bernardino', 'ar_csusb'),
    'KCTCS': ('Kentucky_Community_and_Technical_College_System', 'ar_kctcs'),
    'KY': ('Thomas_More_University', 'ar_ky'),
    'OH': ('University_of_Akron', 'ar_oh')
}

print("\n" + "="*80)
print("ANALYSIS-READY TABLE VERIFICATION")
print("="*80 + "\n")

for school_code, (db_name, ar_table) in DATABASES.items():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', '3306')),
            database=db_name
        )
        
        cursor = conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {ar_table}')
        count = cursor.fetchone()[0]
        
        status = "✓" if count > 0 else "✗"
        print(f"{status} {school_code:6} | {ar_table:10} | {count:,} rows")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"✗ {school_code:6} | {ar_table:10} | ERROR: {str(e)}")

print("\n" + "="*80 + "\n")
