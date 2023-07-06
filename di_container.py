from cloud import ConnectionToCloud
from db import DbTools
from config import get_settings


settings = get_settings()

cloud = ConnectionToCloud('igor233',
                          settings.aws_access_key_id,
                          settings.aws_secret_access_key)

db = DbTools(settings.db_user,
             settings.db_password,
             settings.db_host,
             settings.db_name)


class DiContainer():
    db: DbTools = DbTools()
    cloud: ConnectionToCloud = ConnectionToCloud()


def get_di_container():
    return DiContainer()
