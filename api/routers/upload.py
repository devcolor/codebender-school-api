"""
Upload router for handling file uploads (CSV/Excel) to database tables.
Supports all databases and tables with dynamic column mapping.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Any
from db_operations.connection import get_db_connection, DATABASES
from db_operations.upload_handler import process_upload

router = APIRouter()

# Valid table names
VALID_TABLES = ["cohort", "course", "financial_aid"]


@router.get("/", tags=["Upload"])
async def upload_info():
    """Get information about the upload endpoints."""
    return {
        "message": "Data Upload API",
        "description": "Upload CSV or Excel files to append data to database tables",
        "supported_formats": ["CSV", "Excel (.xlsx, .xls)"],
        "supported_tables": VALID_TABLES,
        "supported_databases": list(DATABASES.keys()),
        "requirements": {
            "dataset_type": "Required field - 'R' for Real data or 'S' for Synthetic data",
            "required_fields": {
                "cohort": ["Student_GUID", "Institution_ID", "Cohort", "Cohort_Term"],
                "course": ["Student_GUID", "Institution_ID", "Cohort", "Cohort_Term"],
                "financial_aid": ["Student_ID", "Institution_ID", "Cohort", "Cohort_Term"]
            },
            "unknown_columns": "Up to 10 unknown columns will be mapped to new_field1-10. More than 10 will result in an error."
        },
        "endpoints": {
            "upload": "POST /{database}/{table}/upload"
        },
        "examples": {
            "AL_cohort": "/upload/AL/cohort/upload",
            "CSUSB_course": "/upload/CSUSB/course/upload",
            "KY_financial_aid": "/upload/KY/financial_aid/upload"
        }
    }


@router.post("/{database}/{table}/upload", tags=["Upload"])
async def upload_data(
    database: str,
    table: str,
    file: UploadFile = File(..., description="CSV or Excel file to upload")
) -> Dict[str, Any]:
    """
    Upload CSV or Excel file to append data to a specific database table.
    
    **Requirements:**
    - File must be CSV or Excel format (.csv, .xlsx, .xls)
    - Must include 'dataset_type' column with value 'R' (Real) or 'S' (Synthetic)
    - Must include all required fields for the table type
    - Unknown columns (up to 10) will be mapped to new_field1 through new_field10
    - Data will be appended to existing table data
    - Upload timestamp will be automatically added
    
    **Parameters:**
    - **database**: Database acronym (AL, CSUSB, KCTCS, KY, OH)
    - **table**: Table name (cohort, course, financial_aid)
    - **file**: CSV or Excel file containing the data
    
    **Returns:**
    - Upload summary with number of rows inserted and column mappings
    
    **Example Response:**
    ```json
    {
        "success": true,
        "table": "cohort",
        "rows_inserted": 150,
        "total_rows": 150,
        "upload_timestamp": "2024-10-27T14:30:00",
        "file_name": "cohort_data.csv",
        "columns_mapped": 25,
        "unknown_columns_mapped": 2,
        "unknown_columns": {
            "custom_field_1": "new_field1",
            "custom_field_2": "new_field2"
        }
    }
    ```
    """
    # Validate database
    if database not in DATABASES:
        raise HTTPException(
            status_code=404,
            detail=f"Database '{database}' not found. Available databases: {list(DATABASES.keys())}"
        )
    
    # Validate table
    if table not in VALID_TABLES:
        raise HTTPException(
            status_code=404,
            detail=f"Table '{table}' not found. Available tables: {VALID_TABLES}"
        )
    
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not (file.filename.endswith('.csv') or 
            file.filename.endswith('.xlsx') or 
            file.filename.endswith('.xls')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only CSV and Excel files (.csv, .xlsx, .xls) are supported."
        )
    
    # Get database name
    database_name = DATABASES[database]
    
    # Process upload
    try:
        with get_db_connection(database_name) as connection:
            result = await process_upload(file, table, connection)
            result["database"] = database
            result["database_name"] = database_name
            return result
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing upload: {str(e)}"
        )


@router.get("/templates/{table}", tags=["Upload"])
async def get_template_info(table: str):
    """
    Get template information for a specific table including required and optional fields.
    
    **Parameters:**
    - **table**: Table name (cohort, course, financial_aid)
    
    **Returns:**
    - Template information with required fields and all available fields
    """
    if table not in VALID_TABLES:
        raise HTTPException(
            status_code=404,
            detail=f"Table '{table}' not found. Available tables: {VALID_TABLES}"
        )
    
    from db_operations.upload_handler import REQUIRED_FIELDS, KNOWN_COLUMNS
    
    return {
        "table": table,
        "required_fields": REQUIRED_FIELDS.get(table, []),
        "all_available_fields": KNOWN_COLUMNS.get(table, []),
        "notes": [
            "dataset_type is REQUIRED: Use 'R' for Real data or 'S' for Synthetic data",
            "created_at timestamp will be automatically added during upload",
            "Unknown columns (up to 10) will be mapped to new_field1 through new_field10",
            "All fields are case-insensitive during upload"
        ]
    }
