import os
import boto3
import pandas as pd
from datetime import datetime
from botocore.exceptions import NoCredentialsError

from dotenv import load_dotenv

load_dotenv()

S3_ACCESSPOINT = os.getenv('S3_ACCESSPOINT')
AWS_PROFILE= os.getenv('AWS_PROFILE')

def load_data(**context):
    ti = context['ti']
    pollution_data = ti.xcom_pull(task_ids='transform_data', key='transform_data_pollution')
    file_name = f'air_pollution_{datetime.now().date()}.csv'
    pollution_data.to_csv(file_name)
    upload_to_aws_s3(
        file_name,
        S3_ACCESSPOINT,
        f'AirPollutionData/{file_name}',
        AWS_PROFILE
    )

# Function Load
def upload_to_aws_s3(local_file, bucket, s3_file, profile_name):
    if profile_name:
        session = boto3.Session(profile_name=profile_name)
    else:
        session = boto3.Session()
    s3 = session.client('s3')
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print(f"Upload Successful: {s3_file}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False