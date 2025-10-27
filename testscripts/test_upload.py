"""
Test script for the data upload feature.
Creates sample CSV files and tests the upload endpoints.
"""
import pandas as pd
import requests
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

# Create test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_DATA_DIR.mkdir(exist_ok=True)


def create_sample_cohort_csv():
    """Create a sample cohort CSV file for testing."""
    data = {
        "Student_GUID": ["TEST001", "TEST002", "TEST003"],
        "Institution_ID": [1, 1, 1],
        "Cohort": ["2024", "2024", "2024"],
        "Cohort_Term": ["Fall", "Fall", "Fall"],
        "Student_Age": ["18-22", "18-22", "23-30"],
        "Gender": ["Male", "Female", "Male"],
        "Race": ["White", "Black or African American", "Hispanic/Latino"],
        "dataset_type": ["S", "S", "S"],
        "custom_field_1": ["Value1", "Value2", "Value3"],
        "custom_field_2": [95.5, 87.2, 91.0]
    }
    
    df = pd.DataFrame(data)
    filepath = TEST_DATA_DIR / "sample_cohort.csv"
    df.to_csv(filepath, index=False)
    print(f"✓ Created sample cohort CSV: {filepath}")
    return filepath


def create_sample_course_csv():
    """Create a sample course CSV file for testing."""
    data = {
        "Student_GUID": ["TEST001", "TEST002", "TEST003"],
        "Institution_ID": [1, 1, 1],
        "Cohort": ["2024", "2024", "2024"],
        "Cohort_Term": ["Fall", "Fall", "Fall"],
        "Academic_Year": ["2024-2025", "2024-2025", "2024-2025"],
        "Course_Prefix": ["MATH", "ENG", "HIST"],
        "Course_Number": [101, 101, 201],
        "Grade": ["A", "B+", "A-"],
        "Number_of_Credits_Attempted": [3, 3, 3],
        "Number_of_Credits_Earned": [3, 3, 3],
        "dataset_type": ["S", "S", "S"]
    }
    
    df = pd.DataFrame(data)
    filepath = TEST_DATA_DIR / "sample_course.csv"
    df.to_csv(filepath, index=False)
    print(f"✓ Created sample course CSV: {filepath}")
    return filepath


def create_sample_financial_aid_csv():
    """Create a sample financial aid CSV file for testing."""
    data = {
        "Student_ID": [1001, 1002, 1003],
        "Institution_ID": [1, 1, 1],
        "Cohort": ["2024", "2024", "2024"],
        "Cohort_Term": ["Fall", "Fall", "Fall"],
        "Academic_Year": ["2024-2025", "2024-2025", "2024-2025"],
        "Cost_of_Attendance": [25000, 25000, 25000],
        "EFC": [5000, 3000, 8000],
        "Total_Federal_Grants": [6000, 6500, 5500],
        "Net_Price": [14000, 15500, 11500],
        "dataset_type": ["S", "S", "S"]
    }
    
    df = pd.DataFrame(data)
    filepath = TEST_DATA_DIR / "sample_financial_aid.csv"
    df.to_csv(filepath, index=False)
    print(f"✓ Created sample financial aid CSV: {filepath}")
    return filepath


def test_upload_endpoint(database, table, filepath):
    """Test uploading a file to the API."""
    url = f"{BASE_URL}/upload/{database}/{table}/upload"
    
    print(f"\n{'='*60}")
    print(f"Testing: {database}/{table}")
    print(f"File: {filepath.name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (filepath.name, f, 'text/csv')}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ SUCCESS!")
            print(f"  - Rows inserted: {result.get('rows_inserted')}")
            print(f"  - Total rows: {result.get('total_rows')}")
            print(f"  - Columns mapped: {result.get('columns_mapped')}")
            print(f"  - Unknown columns: {result.get('unknown_columns_mapped')}")
            if result.get('unknown_columns'):
                print(f"  - Unknown column mapping:")
                for orig, mapped in result['unknown_columns'].items():
                    print(f"    • {orig} → {mapped}")
        else:
            print(f"✗ FAILED!")
            print(f"  Error: {response.json()}")
            
    except requests.exceptions.ConnectionError:
        print(f"✗ CONNECTION ERROR!")
        print(f"  Make sure the API is running at {BASE_URL}")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")


def test_get_template_info(table):
    """Test getting template information."""
    url = f"{BASE_URL}/upload/templates/{table}"
    
    print(f"\n{'='*60}")
    print(f"Getting template info for: {table}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Required fields: {result.get('required_fields')}")
            print(f"✓ Total available fields: {len(result.get('all_available_fields', []))}")
        else:
            print(f"✗ FAILED: {response.json()}")
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")


def test_upload_info():
    """Test getting upload API information."""
    url = f"{BASE_URL}/upload/"
    
    print(f"\n{'='*60}")
    print(f"Getting upload API info")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Message: {result.get('message')}")
            print(f"✓ Supported formats: {result.get('supported_formats')}")
            print(f"✓ Supported tables: {result.get('supported_tables')}")
            print(f"✓ Supported databases: {result.get('supported_databases')}")
        else:
            print(f"✗ FAILED: {response.json()}")
            
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("DATA UPLOAD FEATURE - TEST SCRIPT")
    print("="*60)
    
    # Test API info
    test_upload_info()
    
    # Test template info
    test_get_template_info("cohort")
    test_get_template_info("course")
    test_get_template_info("financial_aid")
    
    # Create sample files
    print(f"\n{'='*60}")
    print("Creating sample test files")
    print(f"{'='*60}")
    cohort_file = create_sample_cohort_csv()
    course_file = create_sample_course_csv()
    financial_aid_file = create_sample_financial_aid_csv()
    
    # Test uploads
    print(f"\n{'='*60}")
    print("Testing file uploads")
    print(f"{'='*60}")
    
    # Test with AL database
    test_upload_endpoint("AL", "cohort", cohort_file)
    test_upload_endpoint("AL", "course", course_file)
    test_upload_endpoint("AL", "financial_aid", financial_aid_file)
    
    print(f"\n{'='*60}")
    print("Test script completed!")
    print(f"{'='*60}\n")
    print("Note: If you see connection errors, make sure the API is running:")
    print("  uvicorn api.main:app --reload")
    print("\nTest files created in:", TEST_DATA_DIR)


if __name__ == "__main__":
    main()
