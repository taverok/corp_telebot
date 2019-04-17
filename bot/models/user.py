from enum import Enum
from typing import Optional, List
from cachetools import cached, TTLCache
from sqlalchemy import asc

from bot.extensions import db


class Role(Enum):
    USER = 1
    ADMIN = 100
    SUPERADMIN = 1000


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger, index=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=False)
    role = db.Column(db.Enum(Role))
    username = db.Column(db.String(255))
    phone = db.Column(db.String(255))

    def __str__(self):
        return f'{self.telegram_id} @{self.username} ({self.name} {self.surname}) {self.phone}'

    def is_admin(self) -> bool:
        try:
            return self.role.value >= Role.ADMIN.value
        except:
            return False

    def to_table_format(self, with_id=False):
        full_name = f'{self.name} {self.surname}'
        username = f'@{self.username}'
        if with_id:
            username += f' ({self.telegram_id})'
        result = f'{full_name:<30}{username:<30}{self.phone:>15} '

        return result


@cached(cache=TTLCache(maxsize=1024, ttl=60))
def get_all_users() -> List[User]:
    return User.query.filter_by(is_active=True).order_by(asc(User.name)).all()


@cached(cache=TTLCache(maxsize=1024, ttl=5))
def find_by_id(_id: int) -> Optional['User']:
    return User.query.filter_by(telegram_id=_id).first()
