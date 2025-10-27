# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# DATA UPLOAD REQUIREMENTS:
# When uploading data via the /upload endpoints, the 'dataset_type' field is REQUIRED:
#   - 'R' = Real data (actual institutional data)
#   - 'S' = Synthetic data (generated/test data)
# This field must be present in all uploaded CSV/Excel files to ensure proper data classification.

# Install system dependencies for MySQL
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
