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
            startDate = st.date_input('Dari', value=datetime(2024,1,1))
        with col2_1:
            endDate = st.date_input('Sampai', value=datetime(2024,1,4)) 

        st.write('Skala Temperatur')
        col1_2, col2_2, col3_2 = st.columns(3)
        with col1_2:
            temperatureScale = st.selectbox('Skala', ('Celsius', 'Fahrenheit'))

        st.write('Skala Timeframe Temperatur')
        col1_2, col2_2, col3_2 = st.columns(3)
        with col1_2:
            timeframeScale = st.selectbox('Skala',('Harian', 'Per Jam', 'Gabungan'))


weatherInfoDataFrame = getDatabaseDataFrame(
    'weather_info'
)

weatherCodeInfoDataFrame = getDatabaseDataFrame(
    'weather_code_info'
)

temperatureDataFrame = getDatabaseDataFrame(
    'temperature'
)

# Format for dataFrame
weatherInfoDataFrame['timestamp'] = pd.to_datetime(weatherInfoDataFrame['timestamp'])
temperatureDataFrame['timestamp'] = pd.to_datetime(temperatureDataFrame['timestamp'])

# Filtered dataFrame
## Filter for timestamp
print(type(startDate), startDate)
try:
    weatherInfoFilteredDataFrame = (
        weatherInfoDataFrame[
            (weatherInfoDataFrame['timestamp'].dt.date >= startDate) &
            (weatherInfoDataFrame['timestamp'].dt.date <= endDate)
        ]
         
    )
    temperatureFilteredDataFrame = (
        temperatureDataFrame[
            (temperatureDataFrame['timestamp'].dt.date >= startDate) &
            (temperatureDataFrame['timestamp'].dt.date <= endDate) 
        ]
    )
except:
    weatherInfoFilteredDataFrame = weatherInfoDataFrame
    temperatureFilteredDataFrame = temperatureDataFrame

## Filter for temperature_unit
if temperatureScale == 'Fahrenheit':
    temperatureFilteredDataFrame['t'] = temperatureFilteredDataFrame['temperature_f']
else:
    temperatureFilteredDataFrame['t'] = temperatureFilteredDataFrame['temperature_c']

# Average Temperature
avgTemperatureMetricsData = temperatureFilteredDataFrame['t'].mean()
# Weather Forecast List
## Merge weather_info & the code
weatherInfoFilteredDataFrame = pd.merge(
    weatherInfoFilteredDataFrame,
    weatherCodeInfoDataFrame,
    how='left',
    left_on='weather_code',
    right_on='code'
)
## Create image URL columns
weatherInfoFilteredDataFrame['img'] = (
    weatherInfoFilteredDataFrame['code'].apply(
        lambda val: f"https://raw.githubusercontent.com/nairkivm/weather-forecast/main/resources/weather_icon/{str(val)}.svg"
    )
)
## Create text_time column
textTimeDict = {0: 'Malam', 6: 'Pagi', 12: 'Siang', 18: 'Sore'}
weatherInfoFilteredDataFrame['txt_time'] = (
    weatherInfoFilteredDataFrame['timestamp'].dt.strftime('%H').apply(
        lambda val: textTimeDict[int(val)]
    )
)
## Create date column
weatherInfoFilteredDataFrame['date'] = (
    weatherInfoFilteredDataFrame['timestamp'].dt.strftime("%d %b '%y")
)
## Sort dataFrame
weatherInfoFilteredDataFrame =(
    weatherInfoFilteredDataFrame
    .sort_values(by='timestamp')
    .reset_index(drop=True)
)

# Temperature TimeFrame
## Create date columns
temperatureFilteredDataFrame['date'] = (
    temperatureFilteredDataFrame['timestamp'].dt.strftime("%d %b '%y")
)
## Create text_time column
temperatureFilteredDataFrame['txt_time'] = (
    temperatureFilteredDataFrame['timestamp'].dt.strftime('%H').apply(
        lambda val: textTimeDict[int(val)]
    )
)
## Sort dataFrame
temperatureFilteredDataFrame = (
    temperatureFilteredDataFrame
    .sort_values(by='timestamp')
    .reset_index(drop=True)
)

# Create a container for the weather summary
with st.container(border=True):
    col1_3, col2_3 = st.columns([1,4])
    with col1_3:
        st.metric(
            '**Temperatur Rerata**',
            f"{avgTemperatureMetricsData:.2f} °"+
            temperatureScale[0]
        )
    with col2_3:
        dateList = list(weatherInfoFilteredDataFrame['date'].unique())
        tabs = st.tabs(dateList)
        i = 0
        for tab in tabs:
            with tab:
                cols = st.columns(4)
                with cols[0]:
                    st.markdown("**Cuaca Pagi (Pukul 6)**")
                    st.image(
                        weatherInfoFilteredDataFrame[
                            (weatherInfoFilteredDataFrame['date'] == dateList[i]) &
                            (weatherInfoFilteredDataFrame['txt_time'] == 'Pagi')
                        ].head(1)['img'].values[0],
                        weatherInfoFilteredDataFrame[
                            (weatherInfoFilteredDataFrame['date'] == dateList[i]) &
                            (weatherInfoFilteredDataFrame['txt_time'] == 'Pagi')
                        ].head(1)['info_id'].values[0],
                        width=100
                    )
                    try:
                        st.markdown(
                            "T = "+
                            temperatureFilteredDataFrame[
                                (temperatureFilteredDataFrame['date'] == dateList[i]) &
                                (temperatureFilteredDataFrame['txt_time'] == 'Pagi')
                            ].head(1)['t'].astype('str').values[0] +
                            " °"+
                            temperatureScale[0]
                        )
                    except:
                        pass
                with cols[1]:
                    st.markdown("**Cuaca Siang (Pukul 12)**")
                    st.image(
                        weatherInfoFilteredDataFrame[
                            (weatherInfoFilteredDataFrame['date'] == dateList[i]) &
                            (weatherInfoFilteredDataFrame['txt_time'] == 'Siang')
                        ].head(1)['img'].values[0],
                        weatherInfoFilteredDataFrame[
                            (weatherInfoFilteredDataFrame['date'] == dateList[i]) &
                            (weatherInfoFilteredDataFrame['txt_time'] == 'Siang')
                        ].head(1)['info_id'].values[0],
                        width=100
                    )
                    try:
                        st.markdown(
                            "T = "+
                            temperatureFilteredDataFrame[
                                (temperatureFilteredDataFrame['date'] == dateList[i]) &
                                (temperatureFilteredDataFrame['txt_time'] == 'Siang')
                            ].head(1)['t'].astype('str').values[0] +
                            " °"+
                            temperatureScale[0]
                        )
                    except:
                        pass
                with cols[2]:
                    st.markdown("**Cuaca Sore (Pukul 18)**")
                    st.image(
                        weatherInfoFilteredDataFrame[
                            (weatherInfoFilteredDataFrame['date'] == dateList[i]) &
                            (weatherInfoFilteredDataFrame['txt_time'] == 'Sore')
                        ].head(1)['img'].values[0],
                        weatherInfoFilteredDataFrame[
                            (weatherInfoFilteredDataFrame['date'] == dateList[i]) &
                            (weatherInfoFilteredDataFrame['txt_time'] == 'Sore')
                        ].head(1)['info_id'].values[0],
                        width=100
                    )
                    try:
                        st.markdown(
                            "T = "+
                            temperatureFilteredDataFrame[
                                (temperatureFilteredDataFrame['date'] == dateList[i]) &
                                (temperatureFilteredDataFrame['txt_time'] == 'Sore')
                            ].head(1)['t'].astype('str').values[0] +
                            " °"+
                            temperatureScale[0]
                        )
                    except:
                        pass
                with cols[3]:
                    st.markdown("**Cuaca Malam (Pukul 0)**")
                    st.image(
                        weatherInfoFilteredDataFrame[
                            (weatherInfoFilteredDataFrame['date'] == dateList[i]) &
                            (weatherInfoFilteredDataFrame['txt_time'] == 'Malam')
                        ].head(1)['img'].values[0],
                        weatherInfoFilteredDataFrame[
                            (weatherInfoFilteredDataFrame['date'] == dateList[i]) &
                            (weatherInfoFilteredDataFrame['txt_time'] == 'Malam')
                        ].head(1)['info_id'].values[0],
                        width=100
                    )
                    try:
                        st.markdown(
                            "T = "+
                            temperatureFilteredDataFrame[
                                (temperatureFilteredDataFrame['date'] == dateList[i]) &
                                (temperatureFilteredDataFrame['txt_time'] == 'Malam')
                            ].head(1)['t'].astype('str').values[0] +
                            " °"+
                            temperatureScale[0]
                        )
                    except:
                        pass
            i += 1

# Set Up for the line chart's scale
if timeframeScale == 'Harian':
    tempDF = (
        temperatureFilteredDataFrame
        .groupby('date')
        ['t']
        .mean()
        .reset_index()
        [['date','t']]
    )
elif timeframeScale == 'Per Jam':
    tempDF = (
        temperatureFilteredDataFrame[
            ['timestamp', 't']
        ]
    )
else:
    tempDF = (
        temperatureFilteredDataFrame
        .groupby('date')
        ['t']
        .mean()
        .reset_index()
        [['date','t']]
    )
    tempDF.columns = ['date','t_daily']
    tempDF = pd.merge(
        temperatureFilteredDataFrame,
        tempDF,
        how='left',
        on='date'
    )
    tempDF = tempDF[['timestamp', 't_daily', 't']]
    tempDF.columns=['timestamp', 't_daily', 't_hourly']

with st.container(border=True):
    if timeframeScale not in ['Harian','Per Jam']:
        tempDF.columns = [
            'Waktu', 
            'Temperatur Harian °'+temperatureScale[0],
            'Temperatur Per Jam °'+temperatureScale[0]
        ]
        st.markdown("**Temperatur dari Waktu ke Waktu**")
        st.line_chart(
            tempDF,
            x="Waktu",
            y=[
                "Temperatur Harian °"+temperatureScale[0],
                "Temperatur Per Jam °"+temperatureScale[0]
            ]
        )
    else:
        tempDF.columns = ['Waktu', 'Temperatur °'+temperatureScale[0]]
        st.markdown("**Temperatur dari Waktu ke Waktu**")
        st.line_chart(
            tempDF,
            x="Waktu",
            y="Temperatur °"+temperatureScale[0]
        )