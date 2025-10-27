#!/usr/bin/env python3
"""
Export full database schema with column names and types
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import json

load_dotenv()

def get_table_schema(db_name, table_name):
    """Get detailed column schema for a table."""
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

        schema = []
        for column in columns:
            col_name, col_type, nullable, key, default, extra = column[:6]
            schema.append({
                "name": col_name,
                "type": col_type,
                "nullable": nullable == "YES",
                "key": key,
                "default": str(default) if default is not None else None,
                "extra": extra
            })

        cursor.close()
        connection.close()
        
        return schema

    except Error as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Use first database as reference
    db = "Bishop_State_Community_College"
    
    tables = ["cohort", "course", "financial_aid"]
    
    result = {}
    for table in tables:
        print(f"\nExporting schema for {table}...")
        schema = get_table_schema(db, table)
        if schema:
            result[table] = schema
            print(f"  Found {len(schema)} columns")
    
    # Save to JSON file
    with open("database_schema.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nSchema exported to database_schema.json")
    
    # Also print a summary
    print("\n" + "="*80)
    print("SCHEMA SUMMARY")
    print("="*80)
    for table, schema in result.items():
        print(f"\n{table.upper()} ({len(schema)} columns):")
        for col in schema:
            print(f"  - {col['name']}: {col['type']}")
