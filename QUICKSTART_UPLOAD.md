# Quick Start Guide - Data Upload Feature

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Database Migration
```bash
python db_operations/add_dynamic_columns.py
```
Press Enter when prompted. This adds the dynamic columns (`new_field1` through `new_field10`) to all tables.

### Step 3: Start the API
```bash
uvicorn api.main:app --reload
```

### Step 4: Test the Upload Feature

#### Option A: Use the Test Script
```bash
python testscripts/test_upload.py
```
This will create sample CSV files and test all upload endpoints.

#### Option B: Use Swagger UI
1. Open browser: `http://localhost:8000/docs`
2. Scroll to "Data Upload" section
3. Click `POST /upload/{database}/{table}/upload`
4. Click "Try it out"
5. Select database: `AL`
6. Select table: `cohort`
7. Upload a CSV file
8. Click "Execute"

#### Option C: Use cURL
```bash
curl -X POST "http://localhost:8000/upload/AL/cohort/upload" \
  -F "file=@your_data.csv"
```

## 📝 Prepare Your CSV File

Your CSV must have:
1. **dataset_type** column with 'R' or 'S'
2. **Required fields** for your table type

### Minimal Example (cohort.csv)
```csv
Student_GUID,Institution_ID,Cohort,Cohort_Term,dataset_type
ABC123,1,2024,Fall,S
DEF456,1,2024,Fall,S
```

### With Custom Fields (cohort.csv)
```csv
Student_GUID,Institution_ID,Cohort,Cohort_Term,dataset_type,my_custom_field
ABC123,1,2024,Fall,S,some_value
DEF456,1,2024,Fall,S,another_value
```
The `my_custom_field` will be automatically mapped to `new_field1`.

## 📋 Required Fields by Table

### Cohort Table
- Student_GUID
- Institution_ID
- Cohort
- Cohort_Term
- dataset_type (R or S)

### Course Table
- Student_GUID
- Institution_ID
- Cohort
- Cohort_Term
- dataset_type (R or S)

### Financial Aid Table
- Student_ID
- Institution_ID
- Cohort
- Cohort_Term
- dataset_type (R or S)

## 🎯 Available Endpoints

### Upload Data
```
POST /upload/{database}/{table}/upload
```
**Databases**: AL, CSUSB, KCTCS, KY, OH  
**Tables**: cohort, course, financial_aid

**Example**:
```
POST /upload/AL/cohort/upload
```

### Get Template Info
```
GET /upload/templates/{table}
```
Returns all available fields for a table.

### Get Upload Info
```
GET /upload/
```
Returns API information and requirements.

## ✅ What Happens When You Upload

1. ✅ File is parsed (CSV or Excel)
2. ✅ `dataset_type` is validated (must be R or S)
3. ✅ Required fields are checked
4. ✅ Columns are mapped (unknown → new_field1-10)
5. ✅ Data is appended to table
6. ✅ Timestamp is automatically added
7. ✅ Summary is returned

## 📊 Example Response

```json
{
  "success": true,
  "database": "AL",
  "table": "cohort",
  "rows_inserted": 150,
  "upload_timestamp": "2024-10-27T14:30:00",
  "file_name": "cohort_data.csv",
  "columns_mapped": 25,
  "unknown_columns_mapped": 2,
  "unknown_columns": {
    "my_custom_field": "new_field1",
    "another_custom": "new_field2"
  }
}
```

## ⚠️ Common Issues

### "Missing required column 'dataset_type'"
**Fix**: Add a `dataset_type` column with values 'R' or 'S' to your CSV.

### "Missing required fields"
**Fix**: Check the error message for which fields are missing. Add them to your CSV.

### "Too many unknown columns"
**Fix**: You have more than 10 columns that don't match the schema. Either:
- Use standard field names from the template
- Reduce the number of custom columns to 10 or fewer

### "Connection refused"
**Fix**: Make sure the API is running:
```bash
uvicorn api.main:app --reload
```

## 📚 More Information

- **Full Documentation**: See `UPLOAD_FEATURE_README.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **API Docs**: `http://localhost:8000/docs`

## 🎉 That's It!

You're ready to upload data. Start with a small test file and verify the data appears in the database.

### Verify Upload
After uploading to the cohort table, check the data:
```bash
curl "http://localhost:8000/al/cohorts?limit=10"
```

Or visit: `http://localhost:8000/docs` and use the GET endpoints.

---

**Need Help?** Check the full documentation in `UPLOAD_FEATURE_README.md`
