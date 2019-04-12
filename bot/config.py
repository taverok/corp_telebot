import os
from os import path
DATA_DIR = str(path.join(path.expanduser("~"), "bot_data"))

DEBUG = True
SECRET_KEY = "changeme"

SQLALCHEMY_DATABASE_URI = f"sqlite:////{DATA_DIR}/bot.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

BOT_TOKEN = 'TOKEN_HERE'

if not path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)
