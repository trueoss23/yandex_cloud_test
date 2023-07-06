import boto3
from config import get_settings
from helpers import resize_image

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

    def upload_file_and_get_url(self, file_name: str, file_name_in_cloud: str) -> str:
        try:
            self.s3.upload_file(file_name, self.bucket, file_name_in_cloud)
            return f'https://storage.yandexcloud.net/{self.bucket}/{file_name_in_cloud}'
        except FileNotFoundError:
            return None
    
    def crete_avatars(self, file_name, file_name_in_cloud):
        file_600_800 = resize_image(file_name, 600, 800, 'png')
        file_32_32 = resize_image(file_name, 32, 32, 'png')
        file_64_64 = resize_image(file_name, 64, 64, 'png')
        file_128_128 = resize_image(file_name, 128, 128, 'png')
        file_256_256 = resize_image(file_name, 256, 256, 'png')
        self.upload_file_and_get_url(file_600_800, f'600_800/{file_name_in_cloud}')
        self.upload_file_and_get_url(file_32_32, f'avatars/32_32/{file_name_in_cloud}')
        self.upload_file_and_get_url(file_64_64, f'avatars/64_64/{file_name_in_cloud}')
        self.upload_file_and_get_url(file_128_128, f'avatars/128_128/{file_name_in_cloud}')
        self.upload_file_and_get_url(file_256_256, f'avatars/256_256/{file_name_in_cloud}')
