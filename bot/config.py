import os
from os import path
DATA_DIR = str(path.join(path.expanduser("~"), "bot_data"))

DEBUG = True
SECRET_KEY = "changeme"

SQLALCHEMY_DATABASE_URI = f"sqlite:////{DATA_DIR}/bot.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)
