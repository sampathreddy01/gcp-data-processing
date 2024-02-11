
## Titanic Data Processing Pipeline

This repository contains code for a data processing pipeline implemented using Airflow. The pipeline processes data related to passengers aboard the Titanic, performs data cleaning and transformation, and stores the processed data in BigQuery for further analysis.

### Description

The pipeline consists of two main components:


1. **Airflow DAG for Orchestration**: The `airflow-script.py` script defines an Airflow DAG (Directed Acyclic Graph) to orchestrate the execution of the Apache Beam pipeline. The DAG is scheduled to run daily and consists of three tasks: a start task, a DataFlowPythonOperator task to execute the Apache Beam pipeline, and an end task. The DataFlowPythonOperator task executes the `dataflow_script_titanic.py` script with the necessary input parameters.

### Usage

To use this pipeline:

1. Set up a Google Cloud Platform (GCP) project and create a BigQuery dataset to store the processed data.

2. Update the `delivered_table_spec` variable in the `dataflow_script_titanic.py` script with the appropriate BigQuery table specification.

3. Update the `options` dictionary in the `airflow-script.py` script with your GCP project ID and region.

4. Configure Airflow to run the DAG by placing the `airflow-script.py` script in your Airflow DAGs folder and starting the Airflow scheduler.

5. Run the Airflow DAG to trigger the execution of the Apache Beam pipeline.

### Dependencies

- Apache Beam (Python SDK)
- Airflow
- Google Cloud Dataflow
- Google Cloud BigQuery
