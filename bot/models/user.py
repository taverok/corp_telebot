import json
from enum import Enum
from typing import Optional

from bot.extensions import db


class Role(Enum):
    SUPERADMIN = 1
    ADMIN = 2
    USER = 10


class User(db.Model):
    """Basic user model
    """
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    role = db.Column(db.Enum(Role))

    def __repr__(self) -> str:
        return json.dumps(dict(self))

    @classmethod
    def find_by_id(cls, _id: int) -> Optional['User']:
        return cls.query.filter_by(id=_id).first()


