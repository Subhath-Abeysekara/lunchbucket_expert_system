import pandas as pd
import boto3
from io import StringIO

# Set your AWS credentials and region
aws_access_key_id = ''
aws_secret_access_key = ''
aws_region = 'ap-south-1'

# Set the S3 bucket and file path
s3_bucket = 'lunchbucket-expert-data'
s3_file_path = 'lunchBucketEXPERT.csv'

# Create a session with boto3
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Create an S3 client
s3 = session.client('s3')

# Read the CSV file from S3 into a pandas dataframe
s3_object = s3.get_object(Bucket=s3_bucket, Key=s3_file_path)
s3_data = s3_object['Body'].read().decode('utf-8')
df = pd.read_csv(StringIO(s3_data))

def getCSV():
    return df

# Print the dataframe
