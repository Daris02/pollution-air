# Air Pollution airflow pipelines

This project is airflow pipelines to load data from weather api and transform it into files data in s3

## Setup
- Clone this repository
- Create a `.env` file in this directory
- Put your api key from [OpenWeather](https://home.openweathermap.org/api_keys) in this `.env` :
  ```txt
    API_KEY=***
  ```
- Copy/Move all files in this project to directory: `~/airflow/dags` and run command:
  ```bash
  airflow standalone
  ```