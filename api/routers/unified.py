from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from ..schemas import CohortRecord, CourseRecord, FinancialAidRecord, LlmRecommendationRecord, AnalysisReadyRecord
from db_operations.connection import get_db_connection, format_records

router = APIRouter()

# Database mappings
DATABASES = {
    "AL": "Bishop_State_Community_College",
    "CSUSB": "California_State_University_San_Bernardino",
    "KCTCS": "Kentucky_Community_and_Technical_College_System",
    "KY": "Thomas_More_University",
    "OH": "University_of_Akron"
}

# Table mappings with their AR table variants
TABLE_MAPPINGS = {
    "cohort": {"table": "cohort", "model": CohortRecord},
    "course": {"table": "course", "model": CourseRecord},
    "financial_aid": {"table": "financial_aid", "model": FinancialAidRecord},
    "llm_recommendations": {"table": "llm_recommendations", "model": LlmRecommendationRecord},
    "analysis_ready": {
        "AL": "ar_al",
        "CSUSB": "ar_csusb",
        "KCTCS": "ar_kctcs",
        "KY": "ar_ky",
        "OH": "ar_oh",
        "model": AnalysisReadyRecord
    }
}

@router.get("/data", response_model=List[Dict[str, Any]])
async def get_unified_data(
    database: str = Query(..., description="Database code: AL, CSUSB, KCTCS, KY, OH"),
    table: str = Query(..., description="Table name: cohort, course, financial_aid, llm_recommendations, analysis_ready"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    student_guid: Optional[str] = Query(None, description="Filter by Student_GUID"),
    cohort: Optional[str] = Query(None, description="Filter by Cohort"),
    academic_year: Optional[str] = Query(None, description="Filter by Academic_Year"),
    institution_id: Optional[int] = Query(None, description="Filter by Institution_ID")
):
    """
    Unified endpoint to query any table from any database with optional filters.
    
    Examples:
    - /unified/data?database=KY&table=cohort&limit=10
    - /unified/data?database=AL&table=course&student_guid=ABC123
    - /unified/data?database=CSUSB&table=analysis_ready&cohort=2020
    - /unified/data?database=KY&table=llm_recommendations&student_guid=ABC123
    """
    
    # Validate database
    if database not in DATABASES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid database. Must be one of: {', '.join(DATABASES.keys())}"
        )
    
    # Validate table
    if table not in TABLE_MAPPINGS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid table. Must be one of: {', '.join(TABLE_MAPPINGS.keys())}"
        )
    
    # Get actual table name (handle analysis_ready special case)
    if table == "analysis_ready":
        actual_table = TABLE_MAPPINGS["analysis_ready"][database]
    else:
        actual_table = TABLE_MAPPINGS[table]["table"]
    
    # Get database name
    db_name = DATABASES[database]
    
    try:
        with get_db_connection(db_name) as connection:
            cursor = connection.cursor(dictionary=True)
            
            # Build query with filters
            query = f"SELECT * FROM {actual_table} WHERE 1=1"
            params = []
            
            # Add filters
            if student_guid:
                # Handle both Student_GUID and student_id columns
                if table == "analysis_ready":
                    query += " AND student_id = %s"
                else:
                    query += " AND Student_GUID = %s"
                params.append(student_guid)
            
            if cohort:
                query += " AND Cohort = %s"
                params.append(cohort)
            
            if academic_year:
                query += " AND Academic_Year = %s"
                params.append(academic_year)
            
            if institution_id:
                query += " AND Institution_ID = %s"
                params.append(institution_id)
            
            # Add ordering and pagination
            query += " ORDER BY id LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            records = cursor.fetchall()
            cursor.close()
            
            return format_records(records)
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching data from {database}.{actual_table}: {str(e)}"
        )

@router.get("/data/count")
async def get_unified_count(
    database: str = Query(..., description="Database code: AL, CSUSB, KCTCS, KY, OH"),
    table: str = Query(..., description="Table name: cohort, course, financial_aid, llm_recommendations, analysis_ready"),
    student_guid: Optional[str] = Query(None, description="Filter by Student_GUID"),
    cohort: Optional[str] = Query(None, description="Filter by Cohort"),
    academic_year: Optional[str] = Query(None, description="Filter by Academic_Year"),
    institution_id: Optional[int] = Query(None, description="Filter by Institution_ID")
):
    """
    Get count of records matching the filters.
    
    Examples:
    - /unified/data/count?database=KY&table=cohort
    - /unified/data/count?database=AL&table=course&student_guid=ABC123
    """
    
    # Validate database
    if database not in DATABASES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid database. Must be one of: {', '.join(DATABASES.keys())}"
        )
    
    # Validate table
    if table not in TABLE_MAPPINGS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid table. Must be one of: {', '.join(TABLE_MAPPINGS.keys())}"
        )
    
    # Get actual table name
    if table == "analysis_ready":
        actual_table = TABLE_MAPPINGS["analysis_ready"][database]
    else:
        actual_table = TABLE_MAPPINGS[table]["table"]
    
    # Get database name
    db_name = DATABASES[database]
    
    try:
        with get_db_connection(db_name) as connection:
            cursor = connection.cursor()
            
            # Build query with filters
            query = f"SELECT COUNT(*) FROM {actual_table} WHERE 1=1"
            params = []
            
            # Add filters
            if student_guid:
                if table == "analysis_ready":
                    query += " AND student_id = %s"
                else:
                    query += " AND Student_GUID = %s"
                params.append(student_guid)
            
            if cohort:
                query += " AND Cohort = %s"
                params.append(cohort)
            
            if academic_year:
                query += " AND Academic_Year = %s"
                params.append(academic_year)
            
            if institution_id:
                query += " AND Institution_ID = %s"
                params.append(institution_id)
            
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            cursor.close()
            
            return {
                "database": database,
                "table": table,
                "count": count,
                "filters": {
                    "student_guid": student_guid,
                    "cohort": cohort,
                    "academic_year": academic_year,
                    "institution_id": institution_id
                }
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error counting records in {database}.{actual_table}: {str(e)}"
        )

@router.get("/databases")
async def list_databases():
    """List all available databases."""
    return {
        "databases": [
            {"code": code, "name": name}
            for code, name in DATABASES.items()
        ]
    }

@router.get("/tables")
async def list_tables():
    """List all available tables."""
    return {
        "tables": list(TABLE_MAPPINGS.keys())
    }
