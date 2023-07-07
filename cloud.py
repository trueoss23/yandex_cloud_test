import boto3
from common.helpers import create_new_file_witn_new_size
from config import get_settings


settings = get_settings()


class ConnectionToCloud():
    def __init__(self, bucket,
                 aws_access_key_id,
                 aws_secret_access_key,
                 endpoint_url):
        self.bucket = bucket
        self.endpoint_url = endpoint_url
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='ru-central1',
            endpoint_url=endpoint_url
        )

    def get_file_names(self, bucket_name):
        for key in self.s3.list_objects(Bucket=bucket_name)['Contents']:
            print((key['Key']))

    def upload_file_and_get_url(self, file_name: str, file_name_in_cloud: str) -> str | None:
        try:
            self.s3.upload_file(file_name, self.bucket, file_name_in_cloud)
            url = f'https://storage.yandexcloud.net/{self.bucket}/{file_name_in_cloud}'
            return url
        except FileNotFoundError:
            return None

    def delete_objects(self, name: str):
        forDeletion = [
                       {'Key': f'source/{name}.jpg'},
                       {'Key': f'avatars/600_800/{name}_600_800.png'},
                       {'Key': f'avatars/32_32/{name}_32_32.png'},
                       {'Key': f'avatars/64_64/{name}_64_64.png'},
                       {'Key': f'avatars/128_128/{name}_128_128.png'},
                       {'Key': f'avatars/256_256/{name}_256_256.png'},
        ]
        self.s3.delete_objects(Bucket=self.bucket,
                               Delete={'Objects': forDeletion})
        return

    def create_avatars(self, file_name, file_name_in_cloud, file_id) -> dict:
        result = {}
        file_600_800 = create_new_file_witn_new_size(file_name, 600, 800, 'png')
        result['file_600_800'] = file_600_800
        file_32_32 = create_new_file_witn_new_size(file_name, 32, 32, 'png')
        result['file_32_32'] = file_32_32
        file_64_64 = create_new_file_witn_new_size(file_name, 64, 64, 'png')
        result['file_64_64'] = file_64_64
        file_128_128 = create_new_file_witn_new_size(file_name, 128, 128, 'png')
        result['file_128_128'] = file_128_128
        file_256_256 = create_new_file_witn_new_size(file_name, 256, 256, 'png')
        result['file_256_256'] = file_256_256
        return result
