# DevColor Schools API

A RESTful API for accessing educational institution data across multiple schools and databases. This service provides standardized access to student, course, and financial aid information.

## Features

- **Multiple Institution Support**: Access data from multiple educational institutions through a unified API
- **Standardized Endpoints**: Consistent API structure across all institutions
- **Pagination**: Built-in support for large datasets
- **Filtering**: Query specific data subsets using query parameters

## Prerequisites

- Python 3.8+
- MySQL/MariaDB
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/syntex-data/devcolor-backend-schools.git
   cd devcolor-backend-schools
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   source venv/bin/activate      # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Copy `.env.example` to `.env` and update with your database credentials:
   ```
   DB_HOST=your_database_host
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_PORT=3306
   ```

## Running the API

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Available Endpoints

### Institution Endpoints

- `GET /` - List all available institutions
- `GET /{institution_code}/` - Get institution details

### Data Endpoints

### Supported Institutions

| Code  | Full Name | Database Name |
|-------|-----------|---------------|
| AL    | Bishop State Community College | `Bishop_State` |
| CSUSB | California State University, San Bernardino | `CSUSB` |
| KCTCS | Kentucky Community and Technical College System | `KCTCS` |
| KY    | Thomas More University | `Thomas_More` |
| OH    | University of Akron | `Akron` |

For each institution, the following endpoints are available:

#### Cohorts
- `GET /{institution_code}/cohorts` - List cohorts
- `GET /{institution_code}/cohort/count` - Get count of cohorts

#### Courses
- `GET /{institution_code}/courses` - List courses
- `GET /{institution_code}/course/count` - Get count of courses

#### Financial Aid
- `GET /{institution_code}/financial-aid` - List financial aid records
- `GET /{institution_code}/financial_aid/count` - Get count of financial aid records

## Query Parameters

### Pagination
- `limit`: Number of records to return (default: 100, max: 1000)
- `offset`: Number of records to skip (default: 0)

Example:
```
/AL/cohorts?limit=10&offset=20
```

## Response Format

All endpoints return JSON responses with the following structure:

```json
{
  "data": [
    // Array of records
  ],
  "count": 123,  // Total number of records
  "page": 1,     // Current page
  "total_pages": 13  // Total number of pages
}
```

## Error Handling

Standard HTTP status codes are used to indicate success or failure:

- `200 OK`: Request was successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Development

### Running Tests

```bash
pytest
```

### Code Style

This project uses `black` for code formatting:

```bash
black .
```

## License

[Your License Here]

## Support

For support, please open an issue in the GitHub repository.

**Install required packages:**
```bash
pip install -r requirements.txt
```

**Configure database connection in `.env`:**
```
DB_HOST=your_database_host
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=3306
```

## Database Structure

Each database in this project contains the following three tables:
- `financial_aid`: Contains financial aid information for students
- `course`: Contains course-related data
- `cohort`: Contains cohort information for tracking student groups

## Database Setup

### 1. Create Databases and Tables
```bash
python db_setup.py
```

This creates 5 databases with 3 tables each:
- Bishop_State_Community_College (AL)
- California_State_University_San_Bernardino (CSUSB)
- Kentucky_Community_and_Technical_College_System (KCTCS)
- Thomas_More_University (KY)
- University_of_Akron (OH)

## Data Summary

**Per Database:**
- Course Records: 200
- Financial Aid Records: 100
- Total per school: 350 records

**Grand Total: 1,750 records across all databases**


## Join-Ready Structure

All tables include a `school` column with matching acronyms (AL, CSUSB, KCTCS, KY, OH) for easy joins across:
- course <-> cohort <-> financial_aid

**Table Relationships:**
- Each table has an auto-incrementing `id` field (PRIMARY KEY) for unique record identification
- Tables can be joined using the `school` column to relate data across institutions
- The `id` fields serve as primary keys for referential integrity when creating relationships
- Example join: `SELECT * FROM course c JOIN cohort co ON c.school = co.school WHERE c.school = 'AL'`

## Fallback Generation

If Ollama is not available or fails, scripts automatically use rule-based synthetic data generation to ensure data is always created.

## Project Structure

```
devcolor-backend/
├── api/
│   ├── __init__.py
│   ├── main.py                 # API routing setup
│   ├── schemas.py              # Pydantic models
│   └── routers/
│       ├── __init__.py
│       ├── al.py               # Alabama institution endpoints
│       ├── csusb.py            # CSUSB institution endpoints
│       ├── kctcs.py            # KCTCS institution endpoints
│       ├── ky.py               # Kentucky institution endpoints
│       └── oh.py               # Ohio institution endpoints
├── db_operations/
│   ├── __init__.py
│   ├── connection.py           # Database connection utilities
│   ├── db_setup.py             # Database setup and table creation
│   ├── generate_db_summary.py  # Database summary generation
│   └── test_db_connection.py   # Database connection testing
├── .env                        # Environment variables (not version controlled)
├── .gitignore
├── check_databases.py          # Database availability checker
├── check_tables.py             # Table structure inspector
├── count_records.py            # Record counting utility
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── test_env.py                 # Environment variable testing
└── test_ky_query.py            # KY database query testing
