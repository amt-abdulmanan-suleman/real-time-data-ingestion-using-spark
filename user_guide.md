# User Guide

## Prerequisites
- Python 3.x
- Apache Spark 3.x with PySpark
- Hadoop binaries (for Windows)
- MySQL JDBC driver (`mysql-connector-j-8.0.33.jar`)
- MySQL database (cloud or local)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install pyspark
```

### 2. Configure Hadoop (Windows Only)
- Download Hadoop binaries for Windows
- Extract to `C:\hadoop`
- Ensure `winutils.exe` is in `C:\hadoop\bin`

### 3. Setup Database
Run the SQL script to create database and table:
```sql
CREATE DATABASE ecommerce_db;

CREATE TABLE events (
    event_id VARCHAR(100) PRIMARY KEY,
    user_id INT,
    product_id INT,
    product_name VARCHAR(100),
    event_type VARCHAR(50),
    price INT,
    event_time TIMESTAMP
);
```

### 4. Update Database Credentials
Edit `spark_streaming_to_postgres.py` and update:
- Database URL
- Username
- Password

## Running the Project

### Step 1: Start Data Generator
Open terminal in project directory:
```bash
cd src
python data_generator.py
```
This generates CSV files every 20 seconds in `streaming_data/` folder.

### Step 2: Start Spark Streaming (New Terminal)
Open a second terminal:
```bash
cd src
spark-submit --jars mysql-connector-j-8.0.33.jar spark_streaming_to_postgres.py
```
This processes CSV files and writes to MySQL in real-time.

### Step 3: Verify Data
Query your MySQL database:
```sql
SELECT * FROM events ORDER BY event_time DESC LIMIT 10;
```

## Stopping the Project
- Press `Ctrl+C` in both terminals to stop the processes
- Data generator and Spark streaming will terminate gracefully

## Troubleshooting
- **Hadoop error**: Verify `HADOOP_HOME` path in `spark_streaming_to_postgres.py`
- **JDBC error**: Ensure MySQL connector JAR is in `src/` directory
- **Connection error**: Check database credentials and network connectivity
