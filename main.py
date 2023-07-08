from fastapi import FastAPI, UploadFile
import uvicorn

from common.di_container import get_di_container

di = get_di_container()
app = FastAPI()


@app.post("/file/upload-file")
def upload_file(file: UploadFile):
    if file.size > 5*10**7:
        return {'file larger then 50 MB'}
    file_name = f'images/{file.filename}'
    with open(file_name, "wb") as f:
        contents = file.file.read()
        f.write(contents)
        result = di.controller_upload_file(file_name, file.content_type)
    di.delete_local_files(file_name)
    return result


@app.get('/delete')
def delete_from_cloud(file_name_without_dot_and_path):
    # di.cloud.delete_objects('cat.jpg')
    di.db.delete_on_file_name('cat')


@app.get('/')
def get_test():
    return {'Hello'}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
