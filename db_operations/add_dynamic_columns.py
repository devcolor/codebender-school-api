"""
Database migration script to add dynamic columns (new_field1 through new_field10)
to cohort, course, and financial_aid tables across all databases.
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

# Database mappings
DATABASES = {
    "AL": "Bishop_State_Community_College",
    "CSUSB": "California_State_University_San_Bernardino", 
    "KCTCS": "Kentucky_Community_and_Technical_College_System",
    "KY": "Thomas_More_University",
    "OH": "University_of_Akron"
}

TABLES = ["cohort", "course", "financial_aid"]

def add_dynamic_columns():
    """Add new_field1 through new_field10 columns to all tables in all databases."""
    
    for db_acronym, db_name in DATABASES.items():
        print(f"\n{'='*60}")
        print(f"Processing database: {db_acronym} ({db_name})")
        print(f"{'='*60}")
        
        try:
            config = DB_CONFIG.copy()
            config["database"] = db_name
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            
            for table in TABLES:
                print(f"\nProcessing table: {table}")
                
                # Check existing columns
                cursor.execute(f"SHOW COLUMNS FROM {table}")
                existing_columns = [col[0] for col in cursor.fetchall()]
                
                # Add new_field1 through new_field10 if they don't exist
                for i in range(1, 11):
                    field_name = f"new_field{i}"
                    
                    if field_name not in existing_columns:
                        try:
                            # Add column as TEXT to handle various data types
                            alter_query = f"ALTER TABLE {table} ADD COLUMN {field_name} TEXT NULL"
                            cursor.execute(alter_query)
                            connection.commit()
                            print(f"  ✓ Added column: {field_name}")
                        except Error as e:
                            print(f"  ✗ Error adding {field_name}: {str(e)}")
                    else:
                        print(f"  - Column {field_name} already exists")
                
                print(f"  Completed table: {table}")
            
            cursor.close()
            connection.close()
            print(f"\n✓ Successfully processed database: {db_acronym}")
            
        except Error as e:
            print(f"\n✗ Error processing database {db_acronym}: {str(e)}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DATABASE MIGRATION: Adding Dynamic Columns")
    print("="*60)
    print("\nThis script will add new_field1 through new_field10 columns")
    print("to cohort, course, and financial_aid tables in all databases.")
    print("\nPress Ctrl+C to cancel, or Enter to continue...")
    
    try:
        input()
        add_dynamic_columns()
        print("\n" + "="*60)
        print("Migration completed successfully!")
        print("="*60 + "\n")
    except KeyboardInterrupt:
        print("\n\nMigration cancelled by user.")
