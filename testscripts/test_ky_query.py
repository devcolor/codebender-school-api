#!/usr/bin/env python3
"""
Test specific queries on KY database to debug the issue
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def test_ky_queries():
    """Test queries on KY database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", "3306")),
            database="Thomas_More_University"
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Test cohorts query
        print("Testing cohorts query...")
        cursor.execute("SELECT * FROM cohort LIMIT 1")
        cohort_result = cursor.fetchall()
        print(f"Cohorts result: {cohort_result}")
        
        # Test courses query  
        print("\nTesting courses query...")
        cursor.execute("SELECT * FROM course LIMIT 1")
        course_result = cursor.fetchall()
        print(f"Courses result: {course_result}")
        
        # Test financial_aid query
        print("\nTesting financial_aid query...")
        cursor.execute("SELECT * FROM financial_aid LIMIT 1")
        financial_aid_result = cursor.fetchall()
        print(f"Financial aid result: {financial_aid_result}")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error testing KY queries: {e}")

if __name__ == "__main__":
    test_ky_queries()
