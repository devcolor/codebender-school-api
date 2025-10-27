"""
Upload handler for processing CSV and Excel files and inserting data into database tables.
Handles dynamic column mapping with support for up to 10 unknown fields.
"""
import pandas as pd
import io
from typing import Dict, List, Tuple, Any
from fastapi import HTTPException, UploadFile
from datetime import datetime
import json

# Required fields for each table type
REQUIRED_FIELDS = {
    "cohort": ["Student_GUID", "Institution_ID", "Cohort", "Cohort_Term"],
    "course": ["Student_GUID", "Institution_ID", "Cohort", "Cohort_Term"],
    "financial_aid": ["Student_ID", "Institution_ID", "Cohort", "Cohort_Term"]
}

# Known columns for each table (from schema)
KNOWN_COLUMNS = {
    "cohort": [
        "Institution_ID", "Cohort", "Student_GUID", "Cohort_Term", "Student_Age",
        "Enrollment_Type", "Enrollment_Intensity_First_Term", "Math_Placement",
        "English_Placement", "Dual_and_Summer_Enrollment", "Race", "Ethnicity",
        "Gender", "First_Gen", "Pell_Status_First_Year", "Attendance_Status_Term_1",
        "Credential_Type_Sought_Year_1", "Program_of_Study_Term_1", "GPA_Group_Term_1",
        "GPA_Group_Year_1", "Number_of_Credits_Attempted_Year_1", "Number_of_Credits_Earned_Year_1",
        "Number_of_Credits_Attempted_Year_2", "Number_of_Credits_Earned_Year_2",
        "Number_of_Credits_Attempted_Year_3", "Number_of_Credits_Earned_Year_3",
        "Number_of_Credits_Attempted_Year_4", "Number_of_Credits_Earned_Year_4",
        "Gateway_Math_Status", "Gateway_English_Status", "AttemptedGatewayMathYear1",
        "AttemptedGatewayEnglishYear1", "CompletedGatewayMathYear1", "CompletedGatewayEnglishYear1",
        "GatewayMathGradeY1", "GatewayEnglishGradeY1", "AttemptedDevMathY1",
        "AttemptedDevEnglishY1", "CompletedDevMathY1", "CompletedDevEnglishY1",
        "Retention", "Persistence", "Years_to_Bachelors_at_cohort_inst_",
        "Years_to_Associates_or_Certificate_at_cohort_inst_", "Years_to_Bachelor_at_other_inst_",
        "Years_to_Associates_or_Certificate_at_other_inst_",
        "Years_of_Last_Enrollment_at_cohort_institution",
        "Years_of_Last_Enrollment_at_other_institution", "Time_to_Credential",
        "Reading_Placement", "Special_Program", "NASPA_First_Generation",
        "Incarcerated_Status", "Military_Status", "Employment_Status",
        "Disability_Status", "Foreign_Language_Completion",
        "First_Year_to_Bachelors_at_cohort_inst_",
        "First_Year_to_Associates_or_Certificate_at_cohort_inst_",
        "First_Year_to_Bachelor_at_other_inst_",
        "First_Year_to_Associates_or_Certificate_at_other_inst_",
        "Program_of_Study_Year_1", "Most_Recent_Bachelors_at_Other_Institution_STATE",
        "Most_Recent_Associates_or_Certificate_at_Other_Ins_dccdad65",
        "Most_Recent_Last_Enrollment_at_Other_institution_STATE",
        "First_Bachelors_at_Other_Institution_STATE",
        "First_Associates_or_Certificate_at_Other_Institution_STATE",
        "Most_Recent_Bachelors_at_Other_Institution_CARNEGIE",
        "Most_Recent_Associates_or_Certificate_at_Other_Ins_5a42b456",
        "Most_Recent_Last_Enrollment_at_Other_institution_CARNEGIE",
        "First_Bachelors_at_Other_Institution_CARNEGIE",
        "First_Associates_or_Certificate_at_Other_Instituti_9c09d367",
        "Most_Recent_Bachelors_at_Other_Institution_LOCALE",
        "Most_Recent_Associates_or_Certificate_at_Other_Ins_9cc1796c",
        "Most_Recent_Last_Enrollment_at_Other_institution_LOCALE",
        "First_Bachelors_at_Other_Institution_LOCALE",
        "First_Associates_or_Certificate_at_Other_Institution_LOCALE",
        "Years_to_Latest_Associates_at_Cohort_Inst",
        "Years_to_Latest_Certificate_at_Cohort_Inst",
        "Years_to_Latest_Associates_at_Other_Inst",
        "Years_to_Latest_Certificate_at_Other_Inst",
        "First_Year_to_Associates_at_Cohort_Inst",
        "First_Year_to_Certificate_at_Cohort_Inst",
        "First_Year_to_Associates_at_Other_Inst",
        "First_Year_to_Certificate_at_Other_Inst",
        "school", "dataset_type", "created_at"
    ],
    "course": [
        "Student_GUID", "Student_Age", "Race", "Ethnicity", "Gender",
        "Institution_ID", "Cohort", "Cohort_Term", "Academic_Year", "Academic_Term",
        "Course_Prefix", "Course_Number", "Section_ID", "Course_Name", "Course_CIP",
        "Course_Type", "Math_or_English_Gateway", "Co_requisite_Course",
        "Course_Begin_Date", "Course_End_Date", "Grade", "Number_of_Credits_Attempted",
        "Number_of_Credits_Earned", "Delivery_Method", "Core_Course", "Core_Course_Type",
        "Core_Competency_Completed", "Enrolled_at_Other_Institutions",
        "Credential_Engine_Identifier", "Course_Instructor_Employment_Status",
        "Course_Instructor_Rank", "Enrollment_Record_at_Other_Institutions_STATEs",
        "Enrollment_Record_at_Other_Institutions_CARNEGIEs",
        "Enrollment_Record_at_Other_Institutions_LOCALEs", "Term_Program_of_Study",
        "school", "dataset_type", "created_at"
    ],
    "financial_aid": [
        "Student_ID", "Institution_ID", "Cohort", "Cohort_Term", "Academic_Year",
        "First_Name", "Middle_Name", "Last_Name", "SSN", "Student_Age", "Date_of_Birth",
        "Dependency_Status", "Housing_Status", "Cost_of_Attendance", "EFC",
        "Total_Institutional_Grants", "Total_State_Grants", "Total_Federal_Grants",
        "Unmet_Need", "Net_Price", "Applied_Aid", "school", "dataset_type", "created_at"
    ]
}


async def parse_uploaded_file(file: UploadFile) -> pd.DataFrame:
    """
    Parse uploaded CSV or Excel file into a pandas DataFrame.
    
    Args:
        file: UploadFile object from FastAPI
        
    Returns:
        pandas DataFrame with the file contents
        
    Raises:
        HTTPException: If file format is unsupported or parsing fails
    """
    try:
        contents = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload CSV or Excel (.xlsx, .xls) files only."
            )
        
        return df
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error parsing file: {str(e)}"
        )


def validate_dataset_type(df: pd.DataFrame) -> None:
    """
    Validate that dataset_type column exists and contains only 'R' or 'S' values.
    
    Args:
        df: pandas DataFrame to validate
        
    Raises:
        HTTPException: If validation fails
    """
    if 'dataset_type' not in df.columns:
        raise HTTPException(
            status_code=400,
            detail="Missing required column 'dataset_type'. Must be 'R' (Real) or 'S' (Synthetic)."
        )
    
    valid_types = {'R', 'S', 'r', 's'}
    invalid_values = df['dataset_type'].dropna().astype(str).str.upper()
    invalid_values = invalid_values[~invalid_values.isin(valid_types)]
    
    if len(invalid_values) > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid dataset_type values found. Must be 'R' (Real) or 'S' (Synthetic). Found: {invalid_values.unique().tolist()}"
        )
    
    # Normalize to uppercase
    df['dataset_type'] = df['dataset_type'].astype(str).str.upper()


def validate_required_fields(df: pd.DataFrame, table_name: str) -> None:
    """
    Validate that all required fields are present in the DataFrame.
    
    Args:
        df: pandas DataFrame to validate
        table_name: Name of the target table
        
    Raises:
        HTTPException: If required fields are missing
    """
    required = REQUIRED_FIELDS.get(table_name, [])
    missing_fields = [field for field in required if field not in df.columns]
    
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required fields for {table_name} table: {missing_fields}"
        )


def map_columns_to_fields(df: pd.DataFrame, table_name: str) -> Tuple[Dict[str, str], List[str]]:
    """
    Map DataFrame columns to database fields, handling unknown columns.
    
    Args:
        df: pandas DataFrame with uploaded data
        table_name: Name of the target table
        
    Returns:
        Tuple of (column_mapping dict, list of error messages)
        
    Raises:
        HTTPException: If more than 10 unknown columns are found
    """
    known_cols = KNOWN_COLUMNS.get(table_name, [])
    known_cols_lower = {col.lower(): col for col in known_cols}
    
    column_mapping = {}
    unknown_columns = []
    
    for col in df.columns:
        col_lower = col.lower()
        
        # Check if it's a known column (case-insensitive)
        if col_lower in known_cols_lower:
            column_mapping[col] = known_cols_lower[col_lower]
        else:
            unknown_columns.append(col)
    
    # Handle unknown columns
    if len(unknown_columns) > 10:
        raise HTTPException(
            status_code=400,
            detail=f"Too many unknown columns ({len(unknown_columns)}). Maximum 10 unknown columns allowed. "
                   f"Unknown columns: {unknown_columns}. Please use appropriate field names from the template."
        )
    
    # Map unknown columns to new_field1 through new_field10
    for idx, col in enumerate(unknown_columns, start=1):
        column_mapping[col] = f"new_field{idx}"
    
    return column_mapping, unknown_columns


def prepare_insert_data(df: pd.DataFrame, column_mapping: Dict[str, str]) -> Tuple[List[str], List[Tuple]]:
    """
    Prepare data for database insertion.
    
    Args:
        df: pandas DataFrame with data
        column_mapping: Dictionary mapping DataFrame columns to database fields
        
    Returns:
        Tuple of (list of database column names, list of value tuples)
    """
    # Replace NaN with None for proper NULL handling
    df = df.where(pd.notnull(df), None)
    
    # Get database column names in order
    db_columns = [column_mapping[col] for col in df.columns if col in column_mapping]
    
    # Prepare values
    values = []
    for _, row in df.iterrows():
        row_values = tuple(row[col] for col in df.columns if col in column_mapping)
        values.append(row_values)
    
    return db_columns, values


def insert_data_to_db(connection, table_name: str, columns: List[str], values: List[Tuple]) -> int:
    """
    Insert data into database table.
    
    Args:
        connection: MySQL database connection
        table_name: Name of the target table
        columns: List of column names
        values: List of value tuples
        
    Returns:
        Number of rows inserted
        
    Raises:
        Exception: If insertion fails
    """
    if not values:
        return 0
    
    cursor = connection.cursor()
    
    # Build INSERT query
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    
    try:
        cursor.executemany(query, values)
        connection.commit()
        rows_inserted = cursor.rowcount
        cursor.close()
        return rows_inserted
    except Exception as e:
        connection.rollback()
        cursor.close()
        raise e


async def process_upload(
    file: UploadFile,
    table_name: str,
    database_connection
) -> Dict[str, Any]:
    """
    Main function to process file upload and insert data into database.
    
    Args:
        file: UploadFile object from FastAPI
        table_name: Name of the target table
        database_connection: MySQL database connection
        
    Returns:
        Dictionary with upload results
        
    Raises:
        HTTPException: If processing fails
    """
    # Parse file
    df = await parse_uploaded_file(file)
    
    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    
    # Validate dataset_type
    validate_dataset_type(df)
    
    # Validate required fields
    validate_required_fields(df, table_name)
    
    # Map columns
    column_mapping, unknown_columns = map_columns_to_fields(df, table_name)
    
    # Prepare data
    db_columns, values = prepare_insert_data(df, column_mapping)
    
    # Insert data
    try:
        rows_inserted = insert_data_to_db(database_connection, table_name, db_columns, values)
        
        result = {
            "success": True,
            "table": table_name,
            "rows_inserted": rows_inserted,
            "total_rows": len(df),
            "upload_timestamp": datetime.now().isoformat(),
            "file_name": file.filename,
            "columns_mapped": len(column_mapping),
            "unknown_columns_mapped": len(unknown_columns)
        }
        
        if unknown_columns:
            result["unknown_columns"] = {
                col: column_mapping[col] for col in unknown_columns
            }
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inserting data into database: {str(e)}"
        )
