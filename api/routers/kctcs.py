from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..schemas import CohortRecord, CourseRecord, FinancialAidRecord, TableCount, DatabaseInfo
from db_operations.connection import get_db_connection, format_records

router = APIRouter()

# Database configuration for KCTCS
DATABASE_NAME = "Kentucky_Community_and_Technical_College_System"
DB_ACRONYM = "KCTCS"
DB_FULL_NAME = "Kentucky Community and Technical College System"

@router.get("/", response_model=DatabaseInfo)
async def get_database_info():
    """Get information about KCTCS database."""
    return DatabaseInfo(
        acronym=DB_ACRONYM,
        full_name=DB_FULL_NAME
    )

@router.get("/cohorts", response_model=List[CohortRecord])
async def get_cohorts(
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip")
):
    """Get cohort records from KCTCS database."""
    try:
        with get_db_connection(DATABASE_NAME) as connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM cohort ORDER BY id LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, offset))
            records = cursor.fetchall()
            cursor.close()
            return format_records(records)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cohorts: {str(e)}")

@router.get("/courses", response_model=List[CourseRecord])
async def get_courses(
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip")
):
    """Get course records from KCTCS database."""
    try:
        with get_db_connection(DATABASE_NAME) as connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM course ORDER BY id LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, offset))
            records = cursor.fetchall()
            cursor.close()
            return format_records(records)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching courses: {str(e)}")

@router.get("/financial-aid", response_model=List[FinancialAidRecord])
async def get_financial_aid(
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip")
):
    """Get financial aid records from KCTCS database."""
    try:
        with get_db_connection(DATABASE_NAME) as connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM financial_aid ORDER BY id LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, offset))
            records = cursor.fetchall()
            cursor.close()
            return format_records(records)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching financial aid: {str(e)}")

@router.get("/{table_name}/count", response_model=TableCount)
async def get_table_count(table_name: str):
    """Get the total count of records in a specific table."""
    valid_tables = ["cohort", "course", "financial_aid"]
    if table_name not in valid_tables:
        raise HTTPException(
            status_code=404,
            detail=f"Table '{table_name}' not found. Available tables: {valid_tables}"
        )
    
    try:
        with get_db_connection(DATABASE_NAME) as connection:
            cursor = connection.cursor()
            query = f"SELECT COUNT(*) as count FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            
            return TableCount(
                database=DB_ACRONYM,
                table=table_name,
                count=result[0] if result else 0
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting records: {str(e)}")
