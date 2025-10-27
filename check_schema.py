#!/usr/bin/env python3
"""
Script to check the actual column structure of tables in each database
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def check_table_schema(db_name, table_name):
    """Check the column structure of a specific table."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", "3306")),
            database=db_name
        )

        cursor = connection.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()

        print(f"\n{table_name.upper()} TABLE in {db_name}:")
        print("=" * 60)
        print(f"{'Column':<30} {'Type':<20} {'Null':<8} {'Key':<10} {'Default':<15}")
        print("-" * 60)

        for column in columns:
            col_name, col_type, nullable, key, default, extra = column[:6]
            null_str = "YES" if nullable == "YES" else "NO"
            print(f"{col_name:<30} {col_type:<20} {null_str:<8} {key:<10} {str(default):<15}")

        print(f"\nTotal columns: {len(columns)}")

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error checking {table_name} in {db_name}: {e}")

if __name__ == "__main__":
    databases = [
        "Bishop_State_Community_College",
        "California_State_University_San_Bernardino",
        "Kentucky_Community_and_Technical_College_System",
        "Thomas_More_University_KY",
        "University_of_Akron_OH"
    ]

    tables_to_check = ["cohort", "course", "financial_aid"]

    for db in databases:
        print(f"\n\n{'='*80}")
        print(f"DATABASE: {db}")
        print('='*80)

        for table in tables_to_check:
            check_table_schema(db, table)
