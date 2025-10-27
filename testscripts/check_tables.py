#!/usr/bin/env python3
"""
Script to check what tables exist in each database
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def check_tables_in_database(db_name):
    """Check what tables exist in a specific database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", "3306")),
            database=db_name
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print(f"\nTables in {db_name}:")
        print("-" * 50)
        if tables:
            for table in tables:
                table_name = table[0]
                print(f"- {table_name}")
        else:
            print("No tables found")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error checking tables in {db_name}: {e}")

if __name__ == "__main__":
    databases = [
        "Bishop_State_Community_College",
        "California_State_University_San_Bernardino", 
        "Kentucky_Community_and_Technical_College_System",
        "Thomas_More_University",
        "University_of_Akron"
    ]
    
    for db in databases:
        check_tables_in_database(db)
