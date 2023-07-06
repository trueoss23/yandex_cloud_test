from fastapi import FastAPI, UploadFile
import uvicorn

from di_container import get_di_container

di = get_di_container
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
        di.cloud.upload_file_and_get_url(file_name, f'source/{file_name_in_cloud}')
        if file.content_type == 'image/jpeg' or file.content_type == 'image/png':
            di.cloud.crete_avatars(file_name, file_name_in_cloud)
    return {'File uploaded'}


@app.get('/')
def get_test():
    try:
        res = di.cloud.upload_file_and_get_url('ar.jpg', 'source/test1.jpg')
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
