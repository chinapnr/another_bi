"""
加载 config.conf 自定义配置文件
此配置优先级高于 config.py 中的配置
"""
import os

from fishbase import conf_as_dict
from superset.singleTon import Singleton


class DataCubeServerSetting(Singleton):
    dt = {}

    def __init__(self):
        DataCubeServerSetting.get_config_info()

    @staticmethod
    def get_config_info():
        config_path = os.path.join("superset", "config", "config.conf")
        conf_info_tuple = conf_as_dict(config_path)
        DataCubeServerSetting.dt = conf_info_tuple[1] if conf_info_tuple[0] else {}


dsc = DataCubeServerSetting()
env_status = dsc.dt["server"]["status"]
conf_info = dsc.dt[env_status]

# redis 配置
REDIS_CONFIG = {
    "host": conf_info["redis_host"],
    "port": conf_info["redis_port"],
    "auth": conf_info["redis_auth"],
    "db": conf_info["redis_db"]
}

# RDS 配置
SQLALCHEMY_DATABASE_URI = conf_info["sqlalchemy_database_uri"]
