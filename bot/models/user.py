import json
from enum import Enum
from typing import Optional
from cachetools import cached, TTLCache

from bot.extensions import db


class Role(Enum):
    USER = 1
    ADMIN = 100
    SUPERADMIN = 1000


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    role = db.Column(db.Enum(Role))

    def __repr__(self) -> str:
        return json.dumps(dict(self))


@cached(cache=TTLCache(maxsize=1024, ttl=5))
def find_by_id(_id: int) -> Optional['User']:
    return User.query.filter_by(telegram_id=_id).first()
