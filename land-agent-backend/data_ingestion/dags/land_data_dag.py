from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable

from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load_land_data import MockLandDataLoader
from fetch_remote_data import MockSatelliteImageFetcher

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_land_data(**context):
    """Task to load land data and save to S3."""
    loader = MockLandDataLoader(num_samples=1000)
    data = loader.generate_geojson()
    
    # Save to S3
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_hook.load_string(
        string_data=str(data),
        key='land_data/raw/land_data.geojson',
        bucket_name=Variable.get('S3_BUCKET_NAME')
    )
    
    return 'land_data/raw/land_data.geojson'

def fetch_satellite_images(**context):
    """Task to fetch satellite images for land parcels."""
    # Get the land data from S3
    s3_hook = S3Hook(aws_conn_id='aws_default')
    land_data = s3_hook.read_key(
        key='land_data/raw/land_data.geojson',
        bucket_name=Variable.get('S3_BUCKET_NAME')
    )
    
    # Extract coordinates from land data
    # In a real implementation, you would parse the GeoJSON and extract coordinates
    # For this mock, we'll use some sample coordinates
    sample_coordinates = [
        (37.7749, -122.4194),
        (37.3382, -121.8863),
        (37.8715, -122.2730)
    ]
    
    # Fetch satellite images
    fetcher = MockSatelliteImageFetcher()
    results = fetcher.fetch_images_batch(sample_coordinates)
    
    # Save metadata to S3
    s3_hook.load_string(
        string_data=str(results),
        key='land_data/raw/satellite_metadata.json',
        bucket_name=Variable.get('S3_BUCKET_NAME')
    )
    
    return 'land_data/raw/satellite_metadata.json'

# Create the DAG
dag = DAG(
    'land_data_ingestion',
    default_args=default_args,
    description='Land data ingestion pipeline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False
)

# Define tasks
load_land_data_task = PythonOperator(
    task_id='load_land_data',
    python_callable=load_land_data,
    provide_context=True,
    dag=dag,
)

fetch_satellite_images_task = PythonOperator(
    task_id='fetch_satellite_images',
    python_callable=fetch_satellite_images,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
load_land_data_task >> fetch_satellite_images_task 