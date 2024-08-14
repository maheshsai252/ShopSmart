import boto3
import os
def extract_bucket_key_and_filename(s3_uri):
    # Remove the 's3://' prefix
    s3_uri = s3_uri.replace('s3://', '')

    # Split the string by the first occurrence of '/'
    parts = s3_uri.split('/', 1)

    # The first part will be the bucket name and the second part will be the key with filename
    bucket_name = parts[0]
    key_with_filename = parts[1] if len(parts) > 1 else ''

    # Split the key with filename by the last occurrence of '/'
    filename_parts = key_with_filename.rsplit('/', 1)

    # The last part will be the filename and the remaining part will be the key
    if len(filename_parts) > 1:
        key = filename_parts[0]
        filename = filename_parts[1]
    else:
        key = ''
        filename = filename_parts[0]

    return bucket_name, key, filename
def download_from_s3(**context) -> str:
    # local_path='./'
    # os.makedirs(local_path, exist_ok=True)
    dags = os.path.join(os.getcwd(), 'dags')
    print(dags)
    local_path = os.path.join(dags, 'resources')

    s3_uri = context['dag_run'].conf['s3_uri']
    run_id = context['dag_run'].run_id
    local_path = os.path.join(local_path, str(run_id))
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
    aws_secret_access_key =  os.getenv('AWS_SECRET_KEY')
    
    s3 = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key)
    # s3_uri = 's3://cfainstitute-learning-outcomes-raw/pdfs/Level1_combined.pdf'
    bucket_name, key,filename = extract_bucket_key_and_filename(s3_uri=s3_uri)

    # temp_file_name = hook.download_file(key=f"{key}/{filename}", bucket_name=bucket_name, local_path=local_path)
    local_file_path = os.path.join(local_path, filename)
    os.makedirs(local_path, exist_ok=True)
    print(local_file_path)
    try:
        s3.download_file(bucket_name, key + '/' + filename, local_file_path)
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        return None
    return filename