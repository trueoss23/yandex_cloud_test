from pydantic import BaseSettings
from functools import lru_cache

import os


class Settings(BaseSettings):
    api_key: str = os.getenv("API_KEY")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_name: str = os.getenv("DB_NAME")
    aws_access_key_id: str = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: str = os.getenv('AWS_SECRET_ACCESS_KEY')
    endpoint_url_cloud: str = os.getenv('ENDPOINT_URL_CLOUD')

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
