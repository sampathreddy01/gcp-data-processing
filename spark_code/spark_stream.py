import logging

from google.cloud import pubsub
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

# Set up logging
logging.basicConfig(level=logging.INFO)

def create_spark_session():
    spark = SparkSession.builder \
        .appName("SparkDataStreaming") \
        .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.23.4") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")
    logging.info("Spark session created successfully!")
    return spark

def connect_to_pubsub(spark):
    try:
        pubsub_client = pubsub.Client()
        topic = pubsub_client.topic("projects/kinetic-bot-424603-i5/topics/test-topic")
        
        subscription = topic.subscription("subscription01")
        # Read from Pub/Sub
        df = spark.readStream \
            .format("pubsub") \
            .option("subscription", subscription.full_name) \
            .load()
        
        logging.info("Pub/Sub dataframe created successfully")
        return df
    
    except Exception as e:
        logging.error(f"Failed to connect to Pub/Sub: {e}")
        return None

def create_selection_df(df):
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("address", StringType(), False),
        StructField("post_code", StringType(), False),
        StructField("email", StringType(), False),
        StructField("username", StringType(), False),
        StructField("registered_date", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("picture", StringType(), False)
    ])

    selection_df = df.selectExpr("CAST(data AS STRING)").select(from_json(col("data"), schema).alias("data")).select("data.*")
    logging.info("Selection dataframe created successfully")
    return selection_df

def write_to_bigquery(df):
    try:
        df.writeStream \
            .format("bigquery") \
            .outputMode("append") \
            .option("checkpointLocation", "gs://sampath1729reddybucketspark/temp/") \
            .option("table", "project_id.dataset_id.table_id") \
            .start()

        logging.info("Writing to BigQuery started")
    except Exception as e:
        logging.error(f"Failed to write to BigQuery: {e}")

if __name__ == "__main__":
    spark = create_spark_session()

    if spark:
        pubsub_df = connect_to_pubsub(spark)

        if pubsub_df:
            selection_df = create_selection_df(pubsub_df)

            if selection_df:
                write_to_bigquery(selection_df)

                spark.streams.awaitAnyTermination()
            else:
                logging.error("Failed to create selection dataframe")
        else:
            logging.error("Failed to connect to Pub/Sub")
    else:
        logging.error("Failed to create Spark session")
