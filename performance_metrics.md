# Performance Metrics Report

## System Configuration
- **Spark Version**: 4.1.1
- **Java Version**: 22.0.1+8-16
- **OS**: Windows 11 (10.0, amd64)
- **Application**: EcommerceStreaming
- **Processing Mode**: Micro-batch streaming
- **Trigger Interval**: File-based (1 file per trigger)
- **Database**: MySQL (Aiven Cloud)
- **Memory Allocated**: 434.4 MiB RAM

## Data Characteristics
- **Batch Size**: 21 events per CSV file (actual)
- **Generation Frequency**: Every 20 seconds
- **Event Schema**: 7 fields (event_id, user_id, product_id, product_name, event_type, price, event_time)
- **File Format**: CSV with header
- **File Size**: ~2KB per file

## Performance Metrics (Actual)

### Throughput
- **Events per batch**: 21 events
- **Input rows per second**: 1.1 - 1.5 rows/sec
- **Processed rows per second**: 1.1 - 1.5 rows/sec
- **Events per minute**: ~63 events
- **Events per hour**: ~3,780 events
- **Daily capacity**: ~90,720 events

### Latency (Measured)
- **Batch 0**: 18,580 ms (18.6 seconds)
- **Batch 1**: 15,890 ms (15.9 seconds)
- **Batch 2**: 15,095 ms (15.1 seconds)
- **Batch 3**: 14,447 ms (14.4 seconds)
- **Average batch duration**: ~16 seconds

### Detailed Timing Breakdown
| Operation | Batch 0 | Batch 1 | Batch 2 | Batch 3 | Avg |
|-----------|---------|---------|---------|---------|-----|
| addBatch (DB write) | 16,352ms | 14,364ms | 13,904ms | 13,293ms | 14.5s |
| queryPlanning | 541ms | 47ms | 22ms | 27ms | 159ms |
| latestOffset | 550ms | 470ms | 401ms | 377ms | 450ms |
| commitOffsets | 568ms | 381ms | 378ms | 369ms | 424ms |
| walCommit | 452ms | 591ms | 367ms | 364ms | 444ms |
| getBatch | 88ms | 24ms | 17ms | 13ms | 36ms |

### Resource Utilization
- **Files processed**: 1 file per trigger (maxFilesPerTrigger=1)
- **Data transformations**: 2 operations (timestamp cast, null filter)
- **Write mode**: Append (no overwrites)
- **Spark shuffle partitions**: 200
- **Block Manager**: 434.4 MiB RAM
- **Checkpoint location**: Temporary (auto-cleanup)

## Bottlenecks & Optimization

### Current Bottlenecks
1. **Database write (addBatch)**: 13-16 seconds (~88% of total time)
2. **Network latency**: Cloud MySQL connection overhead
3. **Query planning**: 541ms on first batch, improves to ~30ms
4. **Sequential processing**: 1 file at a time limits parallelism

### Optimization Opportunities
1. **Batch size**: Increase from 21 to 100+ events per file
2. **maxFilesPerTrigger**: Process multiple files simultaneously
3. **JDBC tuning**: Configure batch insert size and connection pooling
4. **Format upgrade**: Switch from CSV to Parquet
5. **Local database**: Reduce network latency (16s → 2-3s potential)
6. **Checkpoint optimization**: Use persistent checkpoint location

## Scalability Analysis

### Current Scale
- **Sustainable load**: 63 events/minute
- **Processing efficiency**: 1.1-1.5 rows/second
- **Bottleneck**: Database write operations (14.5s average)

### Scale-up Recommendations
1. **Immediate gains** (2-3x throughput):
   - Increase batch size to 100 events
   - Optimize JDBC batch inserts
   - Process 2-3 files per trigger

2. **Medium-term** (5-10x throughput):
   - Migrate to local/regional database
   - Implement connection pooling
   - Use Parquet format

3. **Long-term** (100x+ throughput):
   - Replace file-based streaming with Kafka
   - Implement partitioned processing
   - Add multiple Spark workers

## Reliability Metrics
- **Data loss**: None (file-based streaming with checkpointing)
- **Duplicate handling**: Primary key constraint on event_id
- **Fault tolerance**: Spark automatic retry on failure
- **Data validation**: Null filtering on user_id field

## Summary
The system processes 63 events/minute with 14-16 second batch latency. Database writes consume 88% of processing time. With optimizations (larger batches, JDBC tuning, local database), throughput can increase 5-10x while reducing latency to 2-3 seconds per batch.
