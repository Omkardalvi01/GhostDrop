import logging
import os
from kv_store import set_key
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
    except Exception as e:
        logging.error(e)
        return False

    if not set_key(str(code), obj_name):
        return False

    return True


def download_from_s3(code: int, path: str, bucket_name: str = "ghostdrop"):
    str_code = str(code)
    responses = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=f"{str_code}/")

    for obj in responses.get("Contents", []):
        filename = os.path.join(path, f"{obj['Key'][len(str_code) + 1 :]}")
        s3_client.download_file(bucket_name, obj["Key"], filename)


def delete_files(code: str):

    s3 = boto3.resource("s3")
    bucket = s3.Bucket("ghostdrop")  # type:ignore

    prefix = code + "/"

    try:
        objects_to_delete = bucket.objects.filter(Prefix=prefix)
        response = objects_to_delete.delete()
        print(response)
    except Exception as e:
        logging.error(e)
