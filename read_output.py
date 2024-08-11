import json
import boto3
import os


s3 = boto3.client('s3')

def lambda_handler(event, context):
    read_bucket = os.environ.get("OUTPUT_S3_BUCKET_NAME")
    read_file_path = os.environ.get("OUTPUT_S3_PATH")
    response = s3.get_object(Bucket=read_bucket, Key=read_file_path)
    body = response["Body"].read()
    output = json.loads(body)
    return {
        'statusCode': 200,
        'body': output["appResponse"]
    }
