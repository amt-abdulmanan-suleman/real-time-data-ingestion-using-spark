import os
os.environ['HADOOP_HOME'] = 'C:\\hadoop'

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("EcommerceStreaming") \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .config("spark.sql.streaming.schemaInference", "true") \
    .getOrCreate()

schema = StructType([
    StructField("event_id", StringType()),
    StructField("user_id", IntegerType()),
    StructField("product_id", IntegerType()),
    StructField("product_name", StringType()),
    StructField("event_type", StringType()),
    StructField("price", IntegerType()),
    StructField("event_time", StringType())
])

df = spark.readStream \
    .schema(schema) \
    .option("maxFilesPerTrigger", 1) \
    .csv("file:///C:/Users/AbdulSuleman/Desktop/Data Engineering Upskill Projects/real-time-data-ingestion-using-spark/src/streaming_data")

processed_df = df \
    .withColumn("event_time", col("event_time").cast("timestamp")) \
    .filter(col("user_id").isNotNull())

def write_to_mysql(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:dburl") \
        .option("dbtable", "events") \
        .option("user", "avnadmin") \
        .option("password", "password") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .mode("append") \
        .save()

query = processed_df.writeStream \
    .foreachBatch(write_to_mysql) \
    .outputMode("append") \
    .start()

query.awaitTermination()
