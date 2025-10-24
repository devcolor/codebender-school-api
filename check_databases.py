#!/usr/bin/env python3
"""
Script to check what databases are available on the MySQL server
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def check_available_databases():
    """Check what databases are available on the MySQL server."""
    try:
        # Connect without specifying a database
        connection = mysql.connector.connect(
            host="devcolor00.czqeeakaypfi.us-west-2.rds.amazonaws.com",
            user="admin",
            password="devcolor2025",
            port=3306
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        print("Available databases on the server:")
        print("-" * 50)
        for db in databases:
            db_name = db[0]
            # Skip system databases
            if db_name not in ['information_schema', 'performance_schema', 'mysql', 'sys']:
                print(f"- {db_name}")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error connecting to MySQL: {e}")

if __name__ == "__main__":
    check_available_databases()
