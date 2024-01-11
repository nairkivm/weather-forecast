# weather-forecast

## Description
This project is an end-to-end data engineering pipeline that extracts weather forecast data from [BMKG](https://www.bmkg.go.id/en.html) (Indonesian non-departmental government agency for meteorology, climatology, and geophysics), stores it in a local database, and feeds the data into a dashboard. The project is built entirely in [Python](https://www.python.org/). 

To extract the data, the project uses [BMKG's API](https://api.bmkg.go.id/prakiraan-cuaca), but it faces some challenges as the API is blocked and the [website](https://data.bmkg.go.id/prakiraan-cuaca/) prevents scraping. The project solves this problem by using ["IMPORTHTML"](https://support.google.com/docs/answer/3093339?hl=en) and ["IMPORTXML"](https://support.google.com/docs/answer/3093342?hl=en) formulas from Google Sheets, which can bypass the website's restrictions. This is the [link](https://docs.google.com/spreadsheets/d/1DZdXexhve4Bih_MYW04PYrbKum8luXvgCZBucWtnFf4/copy) to copy the Google Sheets file that was used to extract the data.

After extracting the data, the project stores the raw data in a data warehouse that runs locally. The project does not use S3 storage, instead using local storage as a data warehouse. Then, the project processes the raw data into clean data, using [pandas](https://pandas.pydata.org/) module extensively, and stores it in a database that runs on a local PostgreSQL server. The project uses [psycopg2](https://www.psycopg.org/docs/) module to connect [PostgreSQL](https://www.postgresql.org/docs/) and Python. 

The project also creates a scheduled workflow of extract-load-transform data daily using [Apache Airflow](https://airflow.apache.org/docs/), which runs inside a [Docker](https://docs.docker.com/) container. Finally, the project uses [Streamlit](https://docs.streamlit.io/), an app framework in Python, to display a dashboard that shows the weather forecast and the temperature of [Kab. Kupang, NTT](https://id.wikipedia.org/wiki/Kabupaten_Kupang). For display purposes, the data source comes from this project directory.

Trivia: 
1. This is just a sample project, so the dataset is small. The project deliberately chooses a location and omits other metrics, such as humidity, wind direction, etc. 
2. The project chooses Kab. Kupang, NTT because that is a city where Indonesian National Observatory (at Mount Timau) is located, so this dashboard could be used to track the weather for astronomy observation purpose.

## Architecture
![weather-forecast-architecture](https://github.com/nairkivm/weather-forecast/blob/main/resources/weather-forecast-architecture.drawio.png "weather-forecast Architecture")

## Database ERD
![weather-forecast-erd](https://github.com/nairkivm/weather-forecast/blob/main/resources/weather-forecast-erd.png "weather-forecast Database ERD")

## DAG
![weather-forecast-dag](https://github.com/nairkivm/weather-forecast/blob/main/resources/weather-forecast-dag.png "weather-forecast DAG")

## Dashboard
[![weather-forecast-dashboard](https://github.com/nairkivm/weather-forecast/blob/main/resources/weather-forecast-dashboard.png "weather-forecast Dashboard")](https://nairkivm-weather-forecast-weather-forecast-dashboard.streamlit.app/)


## Resources:
- Weather Data - [Data Prakiraan Cuaca Terbuka BMKG](https://data.bmkg.go.id/prakiraan-cuaca/)
- Project Structure Inspiration - [Surfline Dashboard](https://github.com/andrem8/surf_dash/)
- Docker Compose For Airflow - [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#running-airflow-in-docker)
- Airflow Docker Tutorial - [How to Install and Run Apache Airflow Using Docker in Windows 11 | Airflow Docker #airflow](https://www.youtube.com/watch?v=Sva8rDtlWi4)
- Deploy Airflow - [Deploy Apache Airflow in Multiple Docker Containers](https://towardsdatascience.com/deploy-apache-airflow-in-multiple-docker-containers-7f17b8b3de58)
- Streamlit Tutorial - [Python Streamlit Full Course](https://www.youtube.com/playlist?list=PLa6CNrvKM5QU7AjAS90zCMIwi9RTFNIIW)
- Streamlit Tutorial (2) - [Building a Dashboard web app in Python - Full Streamlit Tutorial](https://www.youtube.com/watch?v=o6wQ8zAkLxc)
