from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from google.cloud import pubsub_v1
import pendulum
import requests
import json
import uuid
import logging

# Define your DAG
default_args = {
    'owner': 'airflow',
    'start_date': pendulum.today('UTC').add(days=-1),
    'retries': 1,
}
dag = DAG(
    'test_composer',
    default_args=default_args,
    description='Fetch data from randomuser API and publish to Pub/Sub',
    schedule='@daily',  # Adjust as necessary
)

# Function to fetch data from the API
def fetch_data_from_api():
    logging.info("Fetching data from the API...")
    response = requests.get('https://randomuser.me/api/')
    if response.status_code == 200:
        response = response.json()
        response = response['results'][0]
        logging.info("Data fetched successfully: %s", response)
        return response
    else:
        logging.error("Failed to fetch data: %s", response.status_code)
        response.raise_for_status()

def format_data(res):
    logging.info("Formatting data...")
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    logging.info("Data formatted: %s", data)
    return data

def print_data_in_console(data):
    logging.info("Printing data in console...")
    logging.info("First Name: %s, Email: %s", data['first_name'], data['email'])

# PythonOperator to fetch data
fetch_task = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data_from_api,
    dag=dag,
)

# PythonOperator to format data
format_task = PythonOperator(
    task_id='format_data',
    python_callable=lambda ti: format_data(ti.xcom_pull(task_ids='fetch_data')),
    dag=dag
)

# PythonOperator to print data
print_task = PythonOperator(
    task_id='print_data',
    python_callable=lambda ti: print_data_in_console(ti.xcom_pull(task_ids='format_data')),
    dag=dag,
)

# Define task dependencies
fetch_task >> format_task >> print_task
