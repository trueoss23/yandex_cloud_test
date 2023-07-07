import os

from cloud import ConnectionToCloud
from db import DbTools
from config import get_settings
from .helpers import get_character_after_last_slash
from .singlton import Singleton


settings = get_settings()


class DiContainer(Singleton):
    db: DbTools = DbTools(
                        settings.db_user,
                        settings.db_password,
                        settings.db_host,
                        settings.db_name
    )
    cloud: ConnectionToCloud = ConnectionToCloud(
                                'igor233',
                                settings.aws_access_key_id,
                                settings.aws_secret_access_key,
                                settings.endpoint_url_cloud,
    )

    def delete_local_files(self, file_name: str):
        split_list = file_name.split('.')
        file_name_without_without_extension = split_list[0]
        print('file_name', file_name)
        print('file_name_without_without_extension', file_name_without_without_extension)
        if len(split_list) > 1:
            if (split_list[1] == 'jpg' or split_list[1] == 'png'):
                os.remove(f'{file_name_without_without_extension}_600_800.png')
                os.remove(f'{file_name_without_without_extension}_32_32.png')
                os.remove(f'{file_name_without_without_extension}_64_64.png')
                os.remove(f'{file_name_without_without_extension}_128_128.png')
                os.remove(f'{file_name_without_without_extension}_256_256.png')
        os.remove(f'{file_name}')

    def controller_upload_file(self, file_name, content_type) -> dict:
        result = {}
        file_name_in_cloud = f'source/{get_character_after_last_slash(file_name)}'
        main_url = self.cloud.upload_file_and_get_url(file_name, file_name_in_cloud)
        if main_url is not None:
            main_id = self.db.add_row_to_files_table(file_type=content_type,
                                                     url=main_url)
            if main_id is not None:
                if content_type == 'image/jpeg' or content_type == 'image/png':
                    avatars_names = self.cloud.create_avatars(file_name, file_name_in_cloud, main_id)
                    for key, value in avatars_names.items():
                        if value is not None:
                            size = key[5:]
                            file_name_in_cloud = f'avatars/{size}/{get_character_after_last_slash(value)}'
                            url = self.cloud.upload_file_and_get_url(value, file_name_in_cloud)
                            if url is not None:
                                try:
                                    self.db.add_row_to_avatars_table(main_id, size, url)
                                    result[f'add_file_avatar_{size}in_db'] = 'OK'
                                except Exception:
                                    result[f'add_file_avatar_{size}in_db'] = 'Error'
                                result[f'add_file_avatar_{size}in_cloud'] = 'OK'
                        else:
                            result[f'add_file_avatar_{size}in_cloud'] = 'Error'
                result['add_file_in_db'] = 'OK'
            else:
                result['add_file_in_db'] = 'Error'
            result['add_file_in_cloud'] = 'OK'
            return result
        else:
            return {'file load Error'}


di = DiContainer()


def get_di_container():
    global di
    return di
