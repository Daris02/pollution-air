# Air Pollution airflow pipelines

This project is airflow pipelines to load data from weather api and transform it into files data in s3

## Setup
- Clone this repository
- Create a `.env` file in this directory
- Put your api key from [OpenWeather](https://home.openweathermap.org/api_keys) and accesspoint of your bucket in aws-s3 in this `.env` :
  ```python
    API_KEY=*** # required
    S3_ACCESSPOINT=*** # required if use aws-s3
    AWS_PROFILE=*** # not required
  ```

    NB: If you used spefic profile AWS account, you can put the name of the profile `AWS_PROFILE`

- Copy/Move all files in this project to directory: `~/airflow/dags` and run command:
  ```bash
  airflow standalone
  ```