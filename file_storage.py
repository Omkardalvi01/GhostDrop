import logging
import os

import boto3
import dotenv

dotenv.load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def upload_to_s3(
    file, code: int, bucket_name: str = "ghostdrop", obj_name: str = ""
) -> bool:
    if not obj_name:
        obj_name = f"{str(code)}/" + os.path.basename(file.filename)

    try:
        s3_client.upload_fileobj(file, bucket_name, obj_name)
        return True
    except Exception as e:
        logging.error(e)
        return False


def download_from_s3(code: int, path:str, bucket_name: str = "ghostdrop"):
    str_code = str(code)
    responses = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=f"{str_code}/")

    
    for obj in responses.get("Contents", []):
        filename = os.path.join(path, f"{obj['Key'][len(str_code)+1:]}") 
        s3_client.download_file(bucket_name, obj['Key'], filename)