from fastapi import FastAPI, HTTPException
import uvicorn

from helpers import download_file_from_yandex_cloud
from config import get_settings
from db import DbTools
from cloud import ConnectionToCloud
from my_exeptions import UncorrectForeignKeyExeptions

settings = get_settings()
cloud = ConnectionToCloud('igor233')
db = DbTools(settings.db_user,
             settings.db_password,
             settings.db_host,
             settings.db_name)

app = FastAPI()


@app.get('/')
def get_test():
    # cloud.upload_file('ar.jpg', 'test.jpg')
    # res = db.add_row_to_files_table('jpg', 'aflajfjweekf')
    try:
        res = db.add_row_to_avatars_table(8, 100)
    except UncorrectForeignKeyExeptions as e:
        return {'Uncorrect Foreign key'}
    return {'id': res}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
