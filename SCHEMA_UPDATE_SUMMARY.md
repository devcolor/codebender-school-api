# Database Schema Update Summary

## Overview
The database has been updated with comprehensive student data schemas. The codebase has been synchronized to match the new database structure.

## Database Structure (Current)

### Cohort Table - 89 Columns
**Core Identifying Fields:**
- `id`, `Institution_ID`, `Cohort`, `Student_GUID`, `Cohort_Term`, `Student_Age`

**Demographics:**
- `Race`, `Ethnicity`, `Gender`, `First_Gen`

**Academic Information:**
- Enrollment details, placement scores, GPA tracking
- Credits attempted/earned across 4 years
- Gateway course completion (Math & English)
- Developmental course tracking
- Retention and persistence metrics

**Completion Tracking:**
- Years to credential at cohort and other institutions
- Separate tracking for Bachelor's, Associate's, and Certificates
- Institution details (STATE, CARNEGIE, LOCALE classifications)

**Special Status:**
- `NASPA_First_Generation`, `Incarcerated_Status`, `Military_Status`
- `Employment_Status`, `Disability_Status`, `Foreign_Language_Completion`

**Metadata:**
- `school`, `dataset_type`, `created_at`

### Course Table - 39 Columns
**Student & Institution:**
- `Student_GUID`, `Institution_ID`, `Cohort`, `Cohort_Term`
- Demographics: `Race`, `Ethnicity`, `Gender`, `Student_Age`

**Course Details:**
- `Course_Prefix`, `Course_Number`, `Section_ID`, `Course_Name`
- `Course_CIP`, `Course_Type`, `Course_Begin_Date`, `Course_End_Date`

**Academic Indicators:**
- `Math_or_English_Gateway`, `Co_requisite_Course`
- `Core_Course`, `Core_Course_Type`, `Core_Competency_Completed`

**Performance:**
- `Grade`, `Number_of_Credits_Attempted`, `Number_of_Credits_Earned`

**Delivery & Transfer:**
- `Delivery_Method`, `Enrolled_at_Other_Institutions`
- External institution tracking (STATE, CARNEGIE, LOCALE)

**Instructor:**
- `Course_Instructor_Employment_Status`, `Course_Instructor_Rank`

**Metadata:**
- `school`, `dataset_type`, `created_at`

### Financial Aid Table - 25 Columns
**Student Identification:**
- `Student_ID`, `Institution_ID`, `Cohort`, `Cohort_Term`, `Academic_Year`

**Personal Information:**
- `First_Name`, `Middle_Name`, `Last_Name`
- `SSN`, `Student_Age`, `Date_of_Birth`

**Financial Status:**
- `Dependency_Status`, `Housing_Status`

**Financial Aid Details:**
- `Cost_of_Attendance`, `EFC` (Expected Family Contribution)
- `Total_Institutional_Grants`, `Total_State_Grants`, `Total_Federal_Grants`
- `Unmet_Need`, `Net_Price`, `Applied_Aid`

**Metadata:**
- `school`, `dataset_type`, `created_at`

## Code Changes Made

### 1. Pydantic Schemas Updated (`api/schemas.py`)
- **CohortRecord**: Updated from 5 fields to 89 fields
- **CourseRecord**: Updated from 6 fields to 39 fields
- **FinancialAidRecord**: Updated from 7 fields to 25 fields
- All fields marked as `Optional` to handle varying data completeness
- Added `Decimal` type import for decimal fields (GPA, completion times, etc.)

### 2. Database Setup Script (`db_operations/db_setup.py`)
- Added documentation header explaining the file contains legacy schema
- Points to `database_schema.json` and `api/schemas.py` for current schema
- Preserved for historical reference

### 3. Connection Handler (`db_operations/connection.py`)
- Updated `format_records()` to properly handle all `Decimal` types
- Now converts all Decimal fields to float for JSON serialization (not just 'amount')

### 4. API Routers (No Changes Required)
- Routers use `SELECT *` which automatically fetches all columns
- Pydantic validation handles field mapping automatically
- All existing endpoints remain compatible

### 5. Schema Export Tool Created
- New file: `export_schema.py` - exports complete schema to JSON
- New file: `database_schema.json` - detailed column definitions with types
- New file: `check_schema.py` - verifies database table structures

## Databases

The system manages 5 institutional databases:
1. **AL** - Bishop_State_Community_College
2. **CSUSB** - California_State_University_San_Bernardino
3. **KCTCS** - Kentucky_Community_and_Technical_College_System
4. **KY** - Thomas_More_University
5. **OH** - University_of_Akron

All databases share the same table structure (cohort, course, financial_aid).

## API Compatibility

All existing API endpoints remain functional:
- `GET /api/{school}/cohorts` - Returns full cohort records with all 89 fields
- `GET /api/{school}/courses` - Returns full course records with all 39 fields
- `GET /api/{school}/financial-aid` - Returns full financial aid records with all 25 fields
- `GET /api/{school}/{table}/count` - Returns record counts

The Pydantic models will automatically validate and serialize the data, excluding any `None` values in responses by default.

## Files Created/Modified

**New Files:**
- `export_schema.py` - Schema export utility
- `check_schema.py` - Schema verification utility
- `database_schema.json` - Complete schema documentation
- `SCHEMA_UPDATE_SUMMARY.md` - This file

**Modified Files:**
- `api/schemas.py` - Updated all record models
- `db_operations/db_setup.py` - Added documentation header
- `db_operations/connection.py` - Enhanced format_records()

## Next Steps (Optional)

Consider these enhancements:
1. Add field-specific filtering to API endpoints
2. Create aggregate endpoints for common queries
3. Add data validation rules beyond type checking
4. Implement caching for frequently accessed data
5. Add search/filter capabilities for large datasets

## Verification

To verify the updates work correctly:
```bash
# Check schema
python check_schema.py

# Export schema to JSON
python export_schema.py

# Test database connections
python db_operations/connection.py
```

---
**Update Date:** 2025-10-27
**Schema Version:** 2.0 (Comprehensive Student Data)
