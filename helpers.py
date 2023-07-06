import requests
from PIL import Image #read the image im = Image.open("sample-image.png") #image size print(im.size)



def get_character_after_last_slash(string):
    parts = string.split('/')
    last_part = parts[-1]
    return last_part


def download_file_from_yandex_cloud(url, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_name = get_character_after_last_slash(url)
        with open(file_name, "wb") as file:
            file.write(response.content)
        print("File is already")
    else:
        print("Error download file")


def resize_image(file_name_image: str, width: int, height: int, format: str) -> bool:
    name = file_name_image.split('.')
    prefix = name[0]
    try:
        im = Image.open(file_name_image)
    except FileNotFoundError as e:
        return False
    size = (width, height)
    out = im.resize(size)
    out.save(f'{prefix}_{width}_{height}.{format}')
    return True


resize_image('cat', 23, 24, 'png')
