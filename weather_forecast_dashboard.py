import streamlit as st
import pandas as pd
import plost

# Import packages
import pandas as pd 
import pytz
from datetime import datetime, timedelta

# Untuk kembali ke directory utama
import sys
import os

from utils.datetime_utils import DatetimeUtils
from services.get_database_data_frame import getDatabaseDataFrame

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.header("Dashboard Cuaca di Kab. Kupang, NTT")

with st.container():
    with st.expander("**Filter Dashboard**"):
        st.write('Tanggal')
        col1_1, col2_1, col3_1, col4_1, col5_1 = st.columns(5)
        with col1_1:
            start_date = st.date_input('Dari', value="today")
        with col2_1:
            end_date = st.date_input('Sampai', value="today") 

        st.write('Satuan Temperatur')
        col1_2, col2_2, col3_2 = st.columns(3)
        with col1_2:
            unit = st.selectbox('Satuan', ('Celsius', 'Fahrenheit'))


weatherInfoDataFrame = getDatabaseDataFrame(
    'weather_info',
    ['id', 'timestamp', 'weather_code'],
    "timestamp >= date(now()) - 7"
)

weatherCodeInfoDataFrame = getDatabaseDataFrame(
    'weather_code_info',
    ['id', 'code', 'info_id'],
    ""
)

temperatureDataFrame = getDatabaseDataFrame(
    'temperature',
    ['id', 'timestamp', 'temperature_c', 'temperature_f'],
    ""
)

# Format for dataFrame
weatherInfoDataFrame['timestamp'] = pd.to_datetime(weatherInfoDataFrame['timestamp'])
temperatureDataFrame['timestamp'] = pd.to_datetime(temperatureDataFrame['timestamp'])

# Filtered dataFrame
## Filter for timestamp
try:
    weatherInfoFilteredDataFrame = (
        (weatherInfoDataFrame['timestamp'].dt.date() >= start_date.date()) &
        (weatherInfoDataFrame['timestamp'].dt.date() <= end_date.date()) 
    )
    temperatureFilteredDataFrame = (
        (temperatureDataFrame['timestamp'].dt.date() >= start_date.date()) &
        (temperatureDataFrame['timestamp'].dt.date() <= end_date.date()) 
    )
except:
    weatherInfoFilteredDataFrame = weatherInfoDataFrame
    temperatureFilteredDataFrame = temperatureDataFrame
## Filter for temperature_unit
if unit == 'Fahrenheit':
    temperatureFilteredDataFrame['t'] = temperatureFilteredDataFrame['temperature_f']
else:
    temperatureFilteredDataFrame['t'] = temperatureFilteredDataFrame['temperature_c']

# Temperatur Rerata
avgTemperatureMetricsData = temperatureFilteredDataFrame['t'].mean()
# List Cuaca
weatherInfoFilteredDataFrame = pd.merge(
    weatherInfoFilteredDataFrame,
    weatherCodeInfoDataFrame,
    how='left',
    left_on='weather_code',
    right_on='code'
)


with st.container():


# Average Temperature 
# - Metrics

# Temperature forecast timeline
# - Line chart

# Weather info 
# - 

