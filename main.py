from fastapi import FastAPI, HTTPException
import uvicorn

from helpers import download_file_from_yandex_cloud
from config import get_settings
from db import DbTools
from cloud import ConnectionToCloud

settings = get_settings()
cloud = ConnectionToCloud('igor233')
db = DbTools(settings.db_user,
             settings.db_password,
             settings.db_host,
             settings.db_name)

app = FastAPI()


@app.get('/')
def get_test():
    cloud.upload_file('ar.jpg', 'test.jpg')
    return {'Ok'}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
