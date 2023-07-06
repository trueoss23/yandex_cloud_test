from fastapi import FastAPI, HTTPException, UploadFile
import uvicorn

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


@app.post("/file/upload-file")
def upload_file(file: UploadFile):
    if file.size > 5*10**7:
        return {'file larger then 50 MB'}
    file_name = f'images/{file.filename}'
    with open(file_name, "wb") as f:
        contents = file.file.read()
        f.write(contents)
        file_name_in_cloud = file.filename
        cloud.upload_file_and_get_url(file_name, f'source/{file_name_in_cloud}')
        if file.content_type == 'image/jpeg' or file.content_type == 'image/png':
            cloud.crete_avatars(file_name, file_name_in_cloud)
    return {'File uploaded'}


@app.get('/')
def get_test():
    try:
        res = cloud.upload_file_and_get_url('ar.jpg', 'source/test1.jpg')
        return {res}
    except FileNotFoundError as e:
        return {'Not Found file'}
    # res = db.add_row_to_files_table('jpg', 'aflajfjweekf')
    # try:
    #     res = db.add_row_to_avatars_table(8, 100)
    # except UncorrectForeignKeyExeptions as e:
    #     return {'Uncorrect Foreign key'}
    # return {'id': res}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
