from pydantic import BaseSettings
from functools import lru_cache

import os


class Settings(BaseSettings):
    api_key: str = os.getenv("API_KEY")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
