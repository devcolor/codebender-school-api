# DevColor Schools API

A FastAPI-based REST API for accessing educational institution data across multiple schools and databases. It provides standardized access to student, course, financial aid, LLM recommendation, and analysis-ready data, plus a flexible data upload pipeline.

## Features

- **Multiple Institution Support** – Unified access to 5 educational institution databases
- **Standardized Endpoints** – Consistent API structure across all institutions
- **Unified Querying** – `/unified` endpoints to query any database/table from a single entrypoint
- **Pagination & Filtering** – Built-in support for large datasets and common filters
- **Data Uploads** – Upload CSV/Excel to append data with dynamic column mapping
- **Analysis-Ready Tables** – Access cleaned, enriched, and join-ready views per school

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL/MariaDB
- pip (Python package manager)

### Installation

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

   Copy `.env.example` to `.env` and update it with your database credentials:
   ```env
   DB_HOST=your_database_host
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_PORT=3306
   ```

### Running the API

Start the development server from the project root:
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`.

### API Documentation

Once the server is running, the interactive docs are available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Overview

The main FastAPI app is defined in `api/main.py` and includes routers for:

| Prefix | Description |
|---|---|
| `/al` | Bishop State Community College |
| `/csusb` | California State University San Bernardino |
| `/kctcs` | Kentucky Community and Technical College System |
| `/ky` | Thomas More University |
| `/oh` | University of Akron |
| `/upload` | Data upload endpoints |
| `/unified` | Unified querying across all databases/tables |

The root endpoint (`GET /`) returns API info, available databases, and key endpoint prefixes.

### Supported Institutions

| Code | Full Name | Database Name |
|---|---|---|
| AL | Bishop State Community College | `Bishop_State_Community_College` |
| CSUSB | California State University, San Bernardino | `California_State_University_San_Bernardino` |
| KCTCS | Kentucky Community and Technical College System | `Kentucky_Community_and_Technical_College_System` |
| KY | Thomas More University | `Thomas_More_University` |
| OH | University of Akron | `University_of_Akron` |

## Per-School Endpoints

Each school has its own router mounted under a **lowercase** prefix (e.g. `/al`, `/csusb`). Every prefix exposes the same set of endpoints, shown below using OH – University of Akron as an example.

- `GET /oh/` – Database info
- `GET /oh/cohorts` – List cohort records
- `GET /oh/courses` – List course records
- `GET /oh/financial-aid` – List financial aid records
- `GET /oh/llm-recommendations` – List LLM recommendation records
- `GET /oh/analysis-ready` – List analysis-ready records (from `ar_oh`)
- `GET /oh/{table_name}/count` – Count records in a specific table, where `table_name` is one of `cohort`, `course`, `financial_aid`, `llm_recommendations`, `ar_oh`

The same pattern applies to `/al`, `/csusb`, `/kctcs`, and `/ky`.

## Unified Endpoints

The `/unified` router lets you query any database/table from a single endpoint, instead of going through school-specific routes.

### `GET /unified/data`

Query data with pagination and optional filters.

**Query parameters:**

| Parameter | Required | Notes |
|---|---|---|
| `database` | Yes | `AL`, `CSUSB`, `KCTCS`, `KY`, `OH` |
| `table` | Yes | `cohort`, `course`, `financial_aid`, `llm_recommendations`, `analysis_ready` |
| `limit` | No | Default 100, max 1000 |
| `offset` | No | Default 0 |
| `student_guid` | No | |
| `cohort` | No | |
| `academic_year` | No | |
| `institution_id` | No | |

**Examples:**

- `/unified/data?database=KY&table=cohort&limit=10`
- `/unified/data?database=AL&table=course&student_guid=ABC123`
- `/unified/data?database=CSUSB&table=analysis_ready&cohort=2020`

### `GET /unified/data/count`

Returns the count of records matching the same filter set as `/unified/data`.

### `GET /unified/databases`

Lists all available databases with codes and full names.

## Data Uploads

Uploads are handled by the `/upload` router and support CSV/Excel files with dynamic column mapping.

### `GET /upload/`

Returns metadata about the upload system, including:

- Supported formats: CSV, Excel (`.csv`, `.xlsx`, `.xls`)
- Supported tables: `cohort`, `course`, `financial_aid`
- Supported databases: `AL`, `CSUSB`, `KCTCS`, `KY`, `OH`
- Required fields per table
- Rules for unknown/dynamic columns

### `POST /upload/{database}/{table}/upload`

Uploads a CSV or Excel file to append data to a specific table.

**Path parameters:**

- `database`: one of `AL`, `CSUSB`, `KCTCS`, `KY`, `OH`
- `table`: one of `cohort`, `course`, `financial_aid`

**Requirements:**

- File must be `.csv`, `.xlsx`, or `.xls`
- Must include a `dataset_type` column with values `R` (real data) or `S` (synthetic data)
- Must include all required fields for the target table
- Up to 10 unknown columns will be mapped to `new_field1`–`new_field10`

**Response includes:** success flag, target table, rows inserted/total rows, upload timestamp, file name, and column mapping details (including unknown columns).

### `GET /upload/templates/{table}`

Returns template information for a specific table (`cohort`, `course`, or `financial_aid`), including required fields and all available fields.

## Pagination & Error Handling

Most list endpoints support:

- `limit` – number of records to return (default: 100, max: 1000)
- `offset` – number of records to skip (default: 0)

Example:
```http
GET /al/cohorts?limit=10&offset=20
```

Standard HTTP status codes indicate success or failure:

- `200 OK` – Request was successful
- `400 Bad Request` – Invalid request parameters
- `404 Not Found` – Resource not found
- `500 Internal Server Error` – Server error (including DB connection issues)

## Database

### Configuration

Database connections are configured in `db_operations/connection.py` and use environment variables declared in `.env`:

```env
DB_HOST=your_database_host
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=3306
```

The `DATABASES` mapping defines the available databases and their names.

### Structure (High Level)

Each institutional database includes, at minimum:

- `cohort` – Detailed cohort and student-level attributes
- `course` – Course enrollment and performance details
- `financial_aid` – Financial aid and cost-of-attendance data
- `llm_recommendations` – LLM-generated recommendations and related metadata
- `ar_*` – Analysis-ready tables, e.g. `ar_al`, `ar_csusb`, `ar_kctcs`, `ar_ky`, `ar_oh`

Common characteristics across tables:

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

## Deployment

### Local Deployment

This is the current default way to run the API, either on a developer machine or a self-managed server.

#### Running with Docker

```bash
docker build -f docker/Dockerfile -t devcolor-backend:latest .
docker run -p 8000:8000 --env-file .env devcolor-backend:latest
```

#### Running with Docker Compose

```bash
# Start services
docker-compose -f docker/docker-compose.yml up -d

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### AWS Deployment

Docker images are built and published to **Amazon ECR** automatically via the GitHub Actions workflow defined in `.github/workflows/docker-build.yml`.

**Triggers:** pushes to `main`/`develop`, and pull requests targeting `main`.

**What the workflow does:**

1. Configures AWS credentials (region `us-west-2`)
2. Logs in to Amazon ECR
3. Builds the image from `docker/Dockerfile`
4. Tags and pushes it to the `devcolor00-school` ECR repository as `:latest`

**Required GitHub secrets:**

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

**Deploying the pushed image with App Runner:**

The workflow includes a commented-out step to trigger a deployment on [AWS App Runner](https://aws.amazon.com/apprunner/) once the image lands in ECR. To enable it:

1. Create an App Runner service pointing at the `devcolor00-school` ECR repository
2. Configure the service's environment variables (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`) and, if the database lives in a VPC, attach a VPC connector so App Runner can reach it
3. Add an `APPRUNNER_SERVICE_ARN` secret to the repository
4. Uncomment the `Deploy to App Runner` step in `.github/workflows/docker-build.yml`

Once enabled, every push to `main` will build, push, and redeploy the service automatically.

**Manual push to ECR** (without the CI workflow):

```bash
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-west-2.amazonaws.com
docker build -f docker/Dockerfile -t <account-id>.dkr.ecr.us-west-2.amazonaws.com/devcolor00-school:latest .
docker push <account-id>.dkr.ecr.us-west-2.amazonaws.com/devcolor00-school:latest
```

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
