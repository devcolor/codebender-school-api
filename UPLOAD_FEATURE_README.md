# Data Upload Feature Documentation

## Overview

The DevColor Backend API now supports uploading CSV and Excel files to append data to existing database tables. This feature includes intelligent column mapping with support for up to 10 unknown/custom fields.

## Features

- ✅ **File Format Support**: CSV, Excel (.xlsx, .xls)
- ✅ **Data Appending**: New data is appended to existing tables (not replaced)
- ✅ **Automatic Timestamps**: Upload timestamp automatically added
- ✅ **Dynamic Column Mapping**: Up to 10 unknown columns mapped to `new_field1` through `new_field10`
- ✅ **Required Field Validation**: Ensures all critical fields are present
- ✅ **Dataset Type Classification**: Required 'R' (Real) or 'S' (Synthetic) designation
- ✅ **Multi-Database Support**: Works with all 5 institutional databases

## Quick Start

### 1. Run Database Migration (First Time Only)

Before using the upload feature, add the dynamic columns to your database:

```bash
python db_operations/add_dynamic_columns.py
```

This adds `new_field1` through `new_field10` columns to all tables in all databases.

### 2. Prepare Your Data File

Your CSV or Excel file must include:

**Required for ALL uploads:**
- `dataset_type`: Must be 'R' (Real data) or 'S' (Synthetic data)

**Required fields by table:**

**Cohort Table:**
- `Student_GUID`
- `Institution_ID`
- `Cohort`
- `Cohort_Term`

**Course Table:**
- `Student_GUID`
- `Institution_ID`
- `Cohort`
- `Cohort_Term`

**Financial Aid Table:**
- `Student_ID`
- `Institution_ID`
- `Cohort`
- `Cohort_Term`

### 3. Upload Your File

**Endpoint Pattern:**
```
POST /upload/{database}/{table}/upload
```

**Example Endpoints:**
- `/upload/AL/cohort/upload`
- `/upload/CSUSB/course/upload`
- `/upload/KY/financial_aid/upload`

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/upload/AL/cohort/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@cohort_data.csv"
```

**Using Python:**
```python
import requests

url = "http://localhost:8000/upload/AL/cohort/upload"
files = {"file": open("cohort_data.csv", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## API Endpoints

### 1. Upload Information
```
GET /upload/
```
Returns information about the upload API, supported formats, and requirements.

### 2. Upload Data
```
POST /upload/{database}/{table}/upload
```
Upload a CSV or Excel file to a specific database table.

**Parameters:**
- `database`: Database acronym (AL, CSUSB, KCTCS, KY, OH)
- `table`: Table name (cohort, course, financial_aid)
- `file`: The CSV or Excel file to upload

**Response Example:**
```json
{
  "success": true,
  "database": "AL",
  "database_name": "Bishop_State_Community_College",
  "table": "cohort",
  "rows_inserted": 150,
  "total_rows": 150,
  "upload_timestamp": "2024-10-27T14:30:00.123456",
  "file_name": "cohort_data.csv",
  "columns_mapped": 25,
  "unknown_columns_mapped": 2,
  "unknown_columns": {
    "custom_field_1": "new_field1",
    "custom_field_2": "new_field2"
  }
}
```

### 3. Get Template Information
```
GET /upload/templates/{table}
```
Returns template information including required and available fields for a table.

**Response Example:**
```json
{
  "table": "cohort",
  "required_fields": [
    "Student_GUID",
    "Institution_ID",
    "Cohort",
    "Cohort_Term"
  ],
  "all_available_fields": [
    "Institution_ID",
    "Cohort",
    "Student_GUID",
    "..."
  ],
  "notes": [
    "dataset_type is REQUIRED: Use 'R' for Real data or 'S' for Synthetic data",
    "created_at timestamp will be automatically added during upload",
    "Unknown columns (up to 10) will be mapped to new_field1 through new_field10",
    "All fields are case-insensitive during upload"
  ]
}
```

## Column Mapping Rules

### Known Columns
- Columns matching existing database fields (case-insensitive) are mapped directly
- Example: `student_guid`, `Student_GUID`, `STUDENT_GUID` all map to `Student_GUID`

### Unknown Columns
- Up to 10 unknown columns are automatically mapped to `new_field1` through `new_field10`
- Mapped in the order they appear in your file
- More than 10 unknown columns will result in an error

**Example:**
```csv
Student_GUID,Institution_ID,Cohort,dataset_type,custom_metric_1,custom_metric_2
ABC123,1,2024,R,95.5,True
```

Maps to:
- `Student_GUID` → `Student_GUID`
- `Institution_ID` → `Institution_ID`
- `Cohort` → `Cohort`
- `dataset_type` → `dataset_type`
- `custom_metric_1` → `new_field1`
- `custom_metric_2` → `new_field2`

## Dataset Type Classification

The `dataset_type` field is **REQUIRED** for all uploads:

- **'R'** = Real data (actual institutional data)
- **'S'** = Synthetic data (generated/test data)

This ensures proper data classification and tracking. Values are case-insensitive ('r' and 'R' both work).

## Error Handling

### Common Errors

**Missing dataset_type:**
```json
{
  "detail": "Missing required column 'dataset_type'. Must be 'R' (Real) or 'S' (Synthetic)."
}
```

**Invalid dataset_type value:**
```json
{
  "detail": "Invalid dataset_type values found. Must be 'R' (Real) or 'S' (Synthetic). Found: ['X', 'Y']"
}
```

**Missing required fields:**
```json
{
  "detail": "Missing required fields for cohort table: ['Student_GUID', 'Institution_ID']"
}
```

**Too many unknown columns:**
```json
{
  "detail": "Too many unknown columns (15). Maximum 10 unknown columns allowed. Unknown columns: [...]. Please use appropriate field names from the template."
}
```

**Invalid file format:**
```json
{
  "detail": "Invalid file format. Only CSV and Excel files (.csv, .xlsx, .xls) are supported."
}
```

## Best Practices

1. **Use Templates**: Call `/upload/templates/{table}` to get the list of available fields
2. **Validate Locally**: Check your file has all required fields before uploading
3. **Start Small**: Test with a small file first (10-20 rows)
4. **Use Known Columns**: Minimize unknown columns by using standard field names
5. **Document Custom Fields**: Keep track of what data you put in `new_field1` through `new_field10`
6. **Set Dataset Type**: Always specify whether data is Real ('R') or Synthetic ('S')

## Example Files

### Minimal Cohort Upload (CSV)
```csv
Student_GUID,Institution_ID,Cohort,Cohort_Term,dataset_type
ABC123,1,2024,Fall,R
DEF456,1,2024,Fall,R
GHI789,1,2024,Fall,R
```

### Cohort Upload with Custom Fields (CSV)
```csv
Student_GUID,Institution_ID,Cohort,Cohort_Term,dataset_type,custom_score,custom_flag
ABC123,1,2024,Fall,S,95.5,true
DEF456,1,2024,Fall,S,87.2,false
```

### Course Upload (Excel)
| Student_GUID | Institution_ID | Cohort | Cohort_Term | Course_Prefix | Course_Number | Grade | dataset_type |
|--------------|----------------|--------|-------------|---------------|---------------|-------|--------------|
| ABC123       | 1              | 2024   | Fall        | MATH          | 101           | A     | R            |
| DEF456       | 1              | 2024   | Fall        | ENG           | 101           | B+    | R            |

## Testing

### Using Swagger UI
1. Navigate to `http://localhost:8000/docs`
2. Find the "Data Upload" section
3. Click on `POST /upload/{database}/{table}/upload`
4. Click "Try it out"
5. Select your database and table
6. Upload your file
7. Click "Execute"

### Using Postman
1. Create a new POST request
2. URL: `http://localhost:8000/upload/AL/cohort/upload`
3. Body → form-data
4. Key: `file` (type: File)
5. Value: Select your CSV/Excel file
6. Send

## Database Schema

After running the migration, each table will have these additional columns:

```sql
new_field1 TEXT NULL
new_field2 TEXT NULL
new_field3 TEXT NULL
new_field4 TEXT NULL
new_field5 TEXT NULL
new_field6 TEXT NULL
new_field7 TEXT NULL
new_field8 TEXT NULL
new_field9 TEXT NULL
new_field10 TEXT NULL
```

Plus the existing fields:
- `dataset_type VARCHAR(1)` - Default: 'S'
- `created_at TIMESTAMP` - Default: current_timestamp()

## Troubleshooting

### Upload fails with "Database connection error"
- Check your `.env` file has correct database credentials
- Ensure the database server is running
- Verify network connectivity

### "Table not found" error
- Ensure you're using the correct table name: `cohort`, `course`, or `financial_aid`
- Table names are case-sensitive in the URL

### Data not appearing after upload
- Check the response to confirm `rows_inserted` > 0
- Query the table to verify: `GET /{database}/{table}?limit=10`
- Check for any validation errors in the response

### File parsing errors
- Ensure your CSV uses commas as delimiters
- Check for special characters or encoding issues
- Try opening the file in Excel and re-saving

## Support

For issues or questions:
1. Check the API documentation: `http://localhost:8000/docs`
2. Review this README
3. Check the application logs
4. Contact the development team

## Version History

- **v1.0.0** (2024-10-27): Initial release
  - CSV and Excel upload support
  - Dynamic column mapping (up to 10 unknown fields)
  - Dataset type classification
  - Multi-database support
  - Automatic timestamp tracking
