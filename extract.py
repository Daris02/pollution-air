import json
import requests
import pandas as pd

def extract(**context):
    demographic = pd.read_csv('Demographic_Data.csv')
    geographic = pd.read_csv('Geographic_Data.csv')

    context['ti'].xcom_push(key='demographic', value=demographic)
    context['ti'].xcom_push(key='geographic', value=geographic)

# Function Extract