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
def download_from_s3(s3_uri) -> str:
    resources = os.path.join(os.getcwd(), 'resources')
    aws_access_key_id =os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    s3 = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key)

    bucket_name, key,filename = extract_bucket_key_and_filename(s3_uri=s3_uri)

    local_file_path = os.path.join(resources, filename)
    print(local_file_path)
    try:
        s3.download_file(bucket_name, filename, local_file_path)
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        return None
    return filename
