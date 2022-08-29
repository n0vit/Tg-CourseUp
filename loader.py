import logging
from config.app_config import AppConfig
from pyrogram import Client
from lib.data.repository import CourseRepository


logger = logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

smart_plugins = dict(root="lib")

repo = CourseRepository()

app = Client('client', AppConfig.api_id, AppConfig.api_hash,phone_number='+79159185242', plugins=smart_plugins)

