from fastapi import FastAPI, HTTPException
import uvicorn

from helpers import download_file
from config import get_settings


settings = get_settings()
# app = FastAPI()
# Пример использования
url = "https://storage.yandexcloud.net/igor233/cat.jpg"
api_key = settings.api_key

download_file(url, api_key)







# if __name__ == '__main__':
#     uvicorn.run("main:app", host="localhost", port=8001, reload=True)
