import traceback
import boto3
from botocore.exceptions import ClientError
import os
import cv2

session = boto3.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "AKIASZWXO4SV64HMLRRD"),
    aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY", "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")
)
BUCKET_NAME = os.environ.get("BUCKET_NAME", "waste-segragation")


def upload_file(file_content, file_name, bucket=BUCKET_NAME):
    try:
        s3_client = boto3.client('s3')
        image_string = cv2.imencode('.jpg', file_content)[1].tostring()
        s3_client.put_object(Bucket = bucket, Key = file_name, Body = image_string)
    except ClientError as e:
        traceback.print_exc()
        return False
    return True


def download_file(key, file_name, bucket=BUCKET_NAME):
    try:
        s3 = boto3.resource('s3')
        s3.Bucket(bucket).download_file(key, file_name)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
