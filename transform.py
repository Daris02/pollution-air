import os
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv('API_KEY')

if not apiKey:
    raise ValueError("API_KEY not found in environment variables")

def transform_data(**context):
    ti = context['ti']
    demographic = ti.xcom_pull(task_ids='extract_data', key='demographic')
    geographic = ti.xcom_pull(task_ids='extract_data', key='geographic')

    pollution_data = pd.merge(geographic, demographic, on='Location')

    coord = pd.DataFrame(
        {
            'lat': [  34.052235, 48.866667,  34.886306, -18.777192,  0.170945,  -9.181352],
            'lon': [-118.243683,  2.333333, 134.379711,  46.854328, 37.903969, -75.002365],
            'Location': ['Los Angeles', 'Paris', 'Tokyo', 'Antananarivo', 'Nairobi', 'Lima']
        })

    pollution_data = pd.merge(pollution_data, coord, on='Location')

    pollution_data['AQI Pollution'] = pollution_data.apply(lambda row: get_polution_aqi_data(row, apiKey), axis=1)
    components_df = pollution_data.apply(lambda row: pd.Series(get_polution_components_data(row, apiKey)), axis=1)

    pollution_data = pollution_data.join(components_df)

    pollution_data.drop(columns='lat', axis=1, inplace=True)
    pollution_data.drop(columns='lon', axis=1, inplace=True)
    pollution_data['date'] = datetime.now().date()

    ti.xcom_push(key='transform_data_pollution', value=pollution_data)


# Function Transform
def get_polution_aqi_data(row, apiKey):
    lat = row['lat']
    lon = row['lon']
    response = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={apiKey}')
    data = response.json()
    return data['list'][0]['main']['aqi']

def get_polution_components_data(row, apiKey):
    lat = row['lat']
    lon = row['lon']
    response = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={apiKey}')
    data = response.json()
    return data['list'][0]['components']

