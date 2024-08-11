import boto3
import os
import json
from dotenv import load_dotenv, find_dotenv

from utils import load_documents, get_summary


load_dotenv(find_dotenv())
s3 = boto3.client('s3')


def lambda_handler(event, context):
    doc_bucket = os.environ.get("DOCUMENT_S3_BUCKET_NAME")
    output_bucket = os.environ.get("OUTPUT_S3_BUCKET_NAME")
    output_file_path = os.environ.get("OUTPUT_S3_PATH")

    response = s3.list_objects_v2(
        Bucket=doc_bucket)
    
    doc_list = response.get('Contents', []) 
    if len(doc_list) > 0:
        document_name = doc_list[0]['Key']
    else:
        print("Error: No documents in s3 bucket")

    try:
        response = s3.get_object(Bucket=doc_bucket, Key=document_name)
        if response['ContentType'] == "application/pdf":
            body = response["Body"]
            documents = load_documents(body)
            message = get_summary(documents)
            message_json = json.dumps({"appResponse": message})
            s3.put_object(Bucket=output_bucket, Key=output_file_path, Body=message_json)
            return {
                'statusCode': 200,
                'body': "Successfully summarized document"
            }
        else:
            print("Error: File is not a pdf")
    except Exception as e:
        print(e)
        raise e

