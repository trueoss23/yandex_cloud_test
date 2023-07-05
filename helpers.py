import requests


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


