*Titanic Data Processing Pipeline*
This repository contains code for a data processing pipeline implemented using Apache Beam and Airflow. The pipeline processes data related to passengers aboard the Titanic, performs data cleaning and transformation, and stores the processed data in BigQuery for further analysis.

Description
The pipeline consists of two main components:

Data Processing with Apache Beam: The beam_script_titanic.py script defines a data processing pipeline using Apache Beam. It reads input data from a CSV file containing information about Titanic passengers, cleans and transforms the data, and filters records based on certain criteria (e.g., passengers who survived). The cleaned and filtered data is then written to BigQuery for storage and analysis.

Airflow DAG for Orchestration: The airflow-script.py script defines an Airflow DAG (Directed Acyclic Graph) to orchestrate the execution of the Apache Beam pipeline. The DAG is scheduled to run daily and consists of three tasks: a start task, a DataFlowPythonOperator task to execute the Apache Beam pipeline, and an end task. The DataFlowPythonOperator task executes the beam_script_titanic.py script with the necessary input parameters.

Usage
To use this pipeline:

Ensure that you have Apache Beam, Airflow, and the necessary Python dependencies installed.

Set up a Google Cloud Platform (GCP) project and create a BigQuery dataset to store the processed data.

Update the delivered_table_spec variable in the beam_script_titanic.py script with the appropriate BigQuery table specification.

Update the options dictionary in the airflow-script.py script with your GCP project ID and region.

Configure Airflow to run the DAG by placing the airflow-script.py script in your Airflow DAGs folder and starting the Airflow scheduler.

Run the Airflow DAG to trigger the execution of the Apache Beam pipeline.

Dependencies
Apache Beam (Python SDK)
Airflow
Google Cloud Dataflow
Google Cloud BigQuery
