# Real-Time Data Ingestion System

## System Components

### 1. Data Generator (`data_generator.py`)
Generates synthetic e-commerce events every 20 seconds:
- 20 events per CSV file
- Random user activity (views/purchases) for 4 products
- Output: `streaming_data/events_<timestamp>.csv`

### 2. Spark Streaming Processor (`spark_streaming_to_postgres.py`)
Processes incoming CSV files in real-time:
- Reads new files as they arrive (1 file per trigger)
- Transforms event_time to timestamp format
- Filters invalid records (null user_id)
- Writes to MySQL in micro-batches

### 3. MySQL Database
Stores processed events in `events` table with schema:
- event_id, user_id, product_id, product_name, event_type, price, event_time

## Data Flow

```
Data Generator → CSV Files → Spark Streaming → MySQL Database
   (every 20s)   streaming_data/   (real-time)    (cloud-hosted)
```

1. Generator creates CSV with 20 events
2. Spark detects and reads new file
3. Data is validated and transformed
4. Records appended to MySQL events table
5. Cycle repeats continuously

## Technology Stack
- Python, Apache Spark, PySpark, MySQL (Aiven), JDBC
