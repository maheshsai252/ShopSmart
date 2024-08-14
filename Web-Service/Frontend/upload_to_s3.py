import boto3
import botocore
import streamlit as st

import os

# AWS credentials
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = 'us-east-2'

# S3 bucket name
BUCKET_NAME = 'chatimages'

# Function to upload file to S3 and return S3 URI
def upload_to_s3(file_path, object_name=None):
    # If S3 object_name is not specified, use file_path
    if object_name is None:
        object_name = os.path.basename(file_path)
    st.write(AWS_ACCESS_KEY_ID)
    # Create S3 client
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:
        # Upload the file
        bucket_name = BUCKET_NAME
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        s3_uri = f"s3://{bucket_name}/{object_name}"
        st.write(s3_uri)
        return s3_uri
    except botocore.exceptions.ClientError as e:
        st.error(f"Failed to upload file to S3: {e}")