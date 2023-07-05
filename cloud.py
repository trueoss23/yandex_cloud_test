import boto3
from config import get_settings


settings = get_settings()


class ConnectionToCloud():
    def __init__(self, bucket):
        self.bucket = bucket
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name='ru-central1',
            endpoint_url='https://storage.yandexcloud.net'
        )

    def get_file_names(self, bucket_name):
        for key in self.s3.list_objects(Bucket=bucket_name)['Contents']:
            print((key['Key']))

    def upload_file(self, file_name: str, file_name_in_cloud: str):
        self.s3.upload_file(file_name, self.bucket, file_name_in_cloud)
