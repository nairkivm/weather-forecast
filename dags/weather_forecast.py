# Import packages
import pandas as pd 
import pytz
from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator

# Untuk kembali ke directory utama
import sys
import os
sys.path.insert(
    0, os.path.abspath(
        os.path.join(
            # os.path.dirname(__file__), '..'
            os.path.dirname(__file__), '..'
        )
    )
)
from configs.g_sheets import GSheets
from utils.datetime_utils import DatetimeUtils
from services.get_source_data_frame import getSourceDataFrame
from services.post_source_to_warehouse_data_frame import postSourceToWarehouseDataFrame
from services.get_warehouse_data_frame import getWarehouseDataFrame
from services.post_warehouse_to_database_data_frame import postWarehouseToDatabaseDataFrame

def importWeatherInfoDataFrame():
    print('path', os.getcwd())
    print('isi dir', os.listdir())
    # Extract Data
    weatherInfoDataFrame = getSourceDataFrame(
        gSheetId=GSheets.weatherInfoSheet.id,
        gSheetGId=GSheets.weatherInfoSheet.gid,
        skiprows=3
    )
    postSourceToWarehouseDataFrame(
        weatherInfoDataFrame,
        'weather info'
    )

def importTemperatureData():
    # Extract Data
    temperatureDataFrame = getSourceDataFrame(
        gSheetId=GSheets.temperatureSheet.id,
        gSheetGId=GSheets.temperatureSheet.gid,
        skiprows=3
    )
    postSourceToWarehouseDataFrame(
        temperatureDataFrame,
        'temperature'
    )

def loadWeatherInfoData():
    # Load from data warehouse
    weatherInfoDataFrame = getWarehouseDataFrame('weather info')
    # Rename columns so they're the same as columns in database
    weatherInfoDataFrame.columns = [
        'timestamp',
        'weather_code'
    ]
    # Transform the timestamos into proper datetime series format
    weatherInfoDataFrame['timestamp'] = (
        weatherInfoDataFrame['timestamp'].apply(DatetimeUtils.formatDatetime)
    )
    # Update/insert dataFrame into database
    postWarehouseToDatabaseDataFrame(
        dataFrame=weatherInfoDataFrame,
        table_name='weather_info',
        primaryKey='timestamp'
    )

def loadTemperatureData():
    # Load from data warehouse
    temperatureDataFrame = getWarehouseDataFrame('temperature')
    # Rename columns so they're the same as columns in database
    temperatureDataFrame.columns = [
        'timestamp',
        'temperature_c',
        'temperature_f'
    ]
    # Transform the timestamos into proper datetime series format
    temperatureDataFrame['timestamp'] = (
        temperatureDataFrame['timestamp'].apply(DatetimeUtils.formatDatetime)
    )
    # Update/insert dataFrame into database
    postWarehouseToDatabaseDataFrame(
        dataFrame=temperatureDataFrame,
        table_name='temperature',
        primaryKey='timestamp'
    )

# initializing the default arguments that we'll pass to our DAG
default_args = {
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    'owner': 'airflow',
}

with DAG(
    'weather-forecast',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args=default_args,
    description='Aggregates booking records for data analysis',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 5),
    catchup=False
) as dag:
    task_1 = PythonOperator(
        task_id='import-weather-info-dataframe',
        python_callable=importWeatherInfoDataFrame
    )
    task_2 = PythonOperator(
        task_id='import-temperature-dataframe',
        python_callable=importTemperatureData
    )
    task_3 = PythonOperator(
        task_id='load-weather-info-dataframe',
        python_callable=loadWeatherInfoData
    )
    task_4 = PythonOperator(
        task_id='load-temperature-dataframe',
        python_callable=loadTemperatureData
    )
    # Run tasks
    task_1 >> task_2 >> task_3 >> task_4