# DevColor Schools API

A FastAPI-based REST API for accessing educational institution data across multiple schools and databases. This service provides standardized access to student, course, financial aid, LLM recommendation, and analysis-ready data, plus a flexible data upload pipeline.

## Features

- **Multiple Institution Support**: Unified access to 5 educational institution databases
- **Standardized Endpoints**: Consistent API structure across all institutions
- **Unified Querying**: `/unified` endpoints to query any database/table from a single entrypoint
- **Pagination & Filtering**: Built-in support for large datasets and common filters
- **Data Uploads**: Upload CSV/Excel to append data with dynamic column mapping
- **Analysis-Ready Tables**: Access cleaned, enriched, and join-ready views per school

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

Start the development server from the project root:
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## High-Level API Structure

The main FastAPI app is defined in `api/main.py` and includes routers for:

- `/al`     – Bishop State Community College
- `/csusb`  – California State University San Bernardino
- `/kctcs`  – Kentucky Community and Technical College System
- `/ky`     – Thomas More University
- `/oh`     – University of Akron
- `/upload` – Data upload endpoints
- `/unified` – Unified querying across all databases/tables

The root endpoint provides a quick overview:

- `GET /` – API info, available databases, and key endpoint prefixes

## Supported Institutions

| Code  | Full Name                                       | Database Name                                       |
|-------|-------------------------------------------------|-----------------------------------------------------|
| AL    | Bishop State Community College                  | `Bishop_State_Community_College`                    |
| CSUSB | California State University, San Bernardino     | `California_State_University_San_Bernardino`        |
| KCTCS | Kentucky Community and Technical College System | `Kentucky_Community_and_Technical_College_System`   |
| KY    | Thomas More University                          | `Thomas_More_University`                            |
| OH    | University of Akron                             | `University_of_Akron`                               |

## Per-School Endpoints

Each school has its own router mounted under a **lowercase** prefix (e.g. `/al`, `/csusb`). Within each prefix, the following endpoints are available (paths use the specific school prefix).

### Example: OH – University of Akron (`/oh`)

- `GET /oh/` – Database info

**Cohorts**

- `GET /oh/cohorts` – List cohort records

**Courses**

- `GET /oh/courses` – List course records

**Financial Aid**

- `GET /oh/financial-aid` – List financial aid records

**LLM Recommendations**

- `GET /oh/llm-recommendations` – List LLM recommendation records

**Analysis-Ready**

- `GET /oh/analysis-ready` – List analysis-ready records (from `ar_oh`)

**Counts**

- `GET /oh/{table_name}/count` – Count records in a specific table  
  `table_name` can be one of: `cohort`, `course`, `financial_aid`, `llm_recommendations`, `ar_oh`

Similar patterns apply for `/al`, `/csusb`, `/kctcs`, and `/ky`.

## Unified Endpoints

The `/unified` router lets you query any database/table from a single endpoint.

### `GET /unified/data`

Query data with pagination and optional filters.

**Query parameters:**

- `database` (required): `AL`, `CSUSB`, `KCTCS`, `KY`, `OH`
- `table` (required): `cohort`, `course`, `financial_aid`, `llm_recommendations`, `analysis_ready`
- `limit` (default 100, max 1000)
- `offset` (default 0)
- `student_guid` (optional)
- `cohort` (optional)
- `academic_year` (optional)
- `institution_id` (optional)

**Examples:**

- `/unified/data?database=KY&table=cohort&limit=10`
- `/unified/data?database=AL&table=course&student_guid=ABC123`
- `/unified/data?database=CSUSB&table=analysis_ready&cohort=2020`

### `GET /unified/data/count`

Return the count of records matching the same filter set as above.

### `GET /unified/databases`

List all available databases with codes and full names.

## Data Upload Feature

Uploads are handled by the `/upload` router and support CSV/Excel files with dynamic column mapping.

### `GET /upload/`

Returns metadata about the upload system:

- Supported formats: CSV, Excel (`.csv`, `.xlsx`, `.xls`)
- Supported tables: `cohort`, `course`, `financial_aid`
- Supported databases: `AL`, `CSUSB`, `KCTCS`, `KY`, `OH`
- Required fields per table
- Rules for unknown/dynamic columns

### `POST /upload/{database}/{table}/upload`

Upload a CSV or Excel file to append data to a specific table.

**Path parameters:**

- `database`: one of `AL`, `CSUSB`, `KCTCS`, `KY`, `OH`
- `table`: one of `cohort`, `course`, `financial_aid`

**Requirements:**

- File must be `.csv`, `.xlsx`, or `.xls`
- Must include a `dataset_type` column with values:
  - `R` – Real data
  - `S` – Synthetic data
- Must include all required fields for the target table
- Up to 10 unknown columns will be mapped to `new_field1`–`new_field10`

**Response includes:**

- Success flag
- Target table
- Rows inserted / total rows
- Upload timestamp
- File name
- Column mapping details (including unknown columns)

### `GET /upload/templates/{table}`

Return template information for a specific table, including required fields and all available fields.

- `table`: `cohort`, `course`, `financial_aid`

## Query Parameters & Pagination

Most list endpoints support:

- `limit`: Number of records to return (default: 100, max: 1000)
- `offset`: Number of records to skip (default: 0)

Example:

```http
GET /al/cohorts?limit=10&offset=20
```

## Error Handling

Standard HTTP status codes are used to indicate success or failure:

- `200 OK` – Request was successful
- `400 Bad Request` – Invalid request parameters
- `404 Not Found` – Resource not found
- `500 Internal Server Error` – Server error (including DB connection issues)

## Docker Setup

### Building the Docker Image

```bash
docker build -f docker/Dockerfile -t devcolor-backend:latest .
```

### Using Docker

1. **Run the container:**
```bash
docker run -p 8000:8000 --env-file .env devcolor-backend:latest
```

### Using Docker Compose

1. **Run with Docker Compose:**
```bash
docker-compose -f docker/docker-compose.yml up -d
```

2. **Stop the services:**
```bash
docker-compose -f docker/docker-compose.yml down
```

## CI/CD with GitHub Actions

This project includes automated Docker image building and deployment using GitHub Actions.

### Setting up GitHub Actions

1. **Create the workflow directory:**
```bash
mkdir -p .github/workflows
```

2. **Create the GitHub Actions workflow file** `.github/workflows/docker-build.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: \\\{\\\{ secrets.DOCKER_USERNAME \\\\}\\\\}
        password: \\\{\\\{ secrets.DOCKER_PASSWORD \\\\}\\\\}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: \\\{\\\{ secrets.DOCKER_USERNAME \\\\}\\\\}/devcolor-backend:prod
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### Required GitHub Secrets

Add the following secrets to your GitHub repository settings:

- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token

### Workflow Triggers

The workflow runs automatically on:
- Pushes to `main` or `develop` branches
- Pull requests to the `main` branch

The Docker image will be tagged and pushed to Docker Hub (or your configured registry).

## Database Configuration

Database connections are configured in `db_operations/connection.py` and use environment variables declared in `.env`:

```env
DB_HOST=your_database_host
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=3306
```

The `DATABASES` mapping defines the available databases and their names.

## Database Structure (High Level)

Each institutional database includes (at minimum):

- `cohort` – Detailed cohort and student-level attributes
- `course` – Course enrollment and performance details
- `financial_aid` – Financial aid and cost-of-attendance data
- `llm_recommendations` – LLM-generated recommendations and related metadata
- `ar_*` analysis-ready tables, for example:
  - `ar_al`, `ar_csusb`, `ar_kctcs`, `ar_ky`, `ar_oh`

Common characteristics:

- Auto-incrementing `id` primary key
- `school` column (e.g. `AL`, `CSUSB`, `KCTCS`, `KY`, `OH`) for join-ready structure
- Shared keys such as `Student_GUID`, `Institution_ID`, `Cohort`, `Academic_Year` enabling cross-table joins

Example join:

```sql
SELECT *
FROM course c
JOIN cohort co
  ON c.school = co.school
WHERE c.school = 'AL';
```

Synthetic data generation and upload utilities ensure that all required tables can be populated even when an LLM backend is not available.

## Project Structure

```
devcolor-backend/
├── api/
│   ├── __init__.py
│   ├── main.py                   # FastAPI app and router registration
│   ├── schemas.py                # Pydantic models
│   └── routers/
│       ├── __init__.py
│       ├── al.py                 # AL endpoints
│       ├── csusb.py              # CSUSB endpoints
│       ├── kctcs.py              # KCTCS endpoints
│       ├── ky.py                 # KY endpoints
│       ├── oh.py                 # OH endpoints
│       ├── unified.py            # Unified querying endpoints
│       └── upload.py             # Data upload endpoints
├── db_operations/
│   ├── __init__.py
│   ├── connection.py             # DB connection utilities and health checks
│   ├── db_setup.py               # Database setup and table creation
│   ├── add_dynamic_columns.py    # Migration for dynamic upload columns
│   ├── upload_handler.py         # Upload processing logic
│   ├── generate_db_summary.py    # Database summary generation
│   ├── populate_all_ar_tables.py # Populate analysis-ready tables
│   ├── populate_ar_ky.py         # Populate KY analysis-ready table
│   └── populate_ar_oh.py         # Populate OH analysis-ready table
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── testscripts/
│   ├── check_databases.py
│   ├── check_schema.py
│   ├── check_tables.py
│   ├── count_records.py
│   └── test_new_endpoints.py
├── main.py                       # Optional helper/entry script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .github/                      # GitHub configuration (CI workflows, etc.)
└── database_schema.json          # Exported database schema
