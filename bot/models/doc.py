import json
from datetime import datetime
from typing import List

from sqlalchemy import asc

from bot.extensions import db


class Document(db.Model):
    """Basic user model
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    icon = db.Column(db.Binary())
    content = db.Column(db.UnicodeText(65000))
    is_private = db.Column(db.Boolean())
    user_id = db.Column(db.BigInteger)
    order_id = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return json.dumps(dict(self))

    @classmethod
    def get_all(cls) -> List['Document']:
        return (cls.query
                .order_by(asc(Document.order_id))
                .order_by(asc(Document.created_at))
                .all())


