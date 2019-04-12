"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_migrate import Migrate



db = SQLAlchemy()
migrate = Migrate(compare_type=True)
pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
