import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from fastapi import HTTPException

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

@contextmanager
def get_db_connection(database_name: str):
    """Context manager for database connections."""
    connection = None
    try:
        config = DB_CONFIG.copy()
        config["database"] = database_name
        connection = mysql.connector.connect(**config)
        yield connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
    finally:
        if connection and connection.is_connected():
            connection.close()

def format_records(records):
    """Format database records for JSON response."""
    from decimal import Decimal
    
    for record in records:
        for key, value in record.items():
            if hasattr(value, 'strftime'):  # datetime objects
                record[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, Decimal):  # decimal values
                record[key] = float(value)
    return records

def test_all_connections():
    """Test connectivity to all databases."""
    health_status = {
        "api": "healthy",
        "timestamp": None,
        "databases": {}
    }
    
    from datetime import datetime
    health_status["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for acronym, db_name in DATABASES.items():
        try:
            with get_db_connection(db_name) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                cursor.close()
                health_status["databases"][acronym] = {
                    "status": "connected",
                    "database": db_name
                }
        except Exception as e:
            health_status["databases"][acronym] = {
                "status": "error",
                "database": db_name,
                "error": str(e)
            }
    
    import json
    print(json.dumps(health_status, indent=2))
    return health_status

if __name__ == "__main__":
    test_all_connections()
