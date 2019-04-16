import json
from datetime import datetime
from typing import List, Union

from sqlalchemy import asc, ForeignKey

from bot.extensions import db
from bot.models.exceptions import ValidationException


class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    icon = db.Column(db.Binary())
    content = db.Column(db.UnicodeText(65000))
    is_private = db.Column(db.Boolean(), default=True)
    is_visible = db.Column(db.Boolean(), default=True)
    user_id = db.Column(db.BigInteger)
    order_id = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    parent_id = db.Column(db.Integer, ForeignKey('document.id'))
    parent = db.relationship('Document', remote_side=id, backref='sub_documents')

    def __repr__(self) -> str:
        return json.dumps(dict(self))

    @classmethod
    def find_all_by_parent_id(cls, parent_id=None) -> List['Document']:
        return (cls.query
                .filter_by(parent_id=parent_id)
                .order_by(asc(Document.order_id))
                .order_by(asc(Document.created_at))
                .all())

    @classmethod
    def find_by_id(cls, _id=None) -> 'Document':
        return (cls.query
                .filter_by(id=_id)
                .order_by(asc(Document.order_id))
                .order_by(asc(Document.created_at))
                .first())

    @classmethod
    def from_json(cls, data: Union[dict, list], from_user_id: int) -> List['Document']:
        if type(data) == dict:
            data = [data]

        docs_list = []
        for doc in data:
            required_keys = ('title', 'content')

            if len(doc.keys() & ('title', 'content')) < len(required_keys):
                raise ValidationException(f"All required fields must be set {required_keys}")

            document = Document(
                title=doc.get('title'),
                icon=doc.get('icon', "").encode(),
                content=doc.get('content'),
                user_id=from_user_id
            )

            if 'sub' in doc:
                subs = cls.from_json(doc['sub'], from_user_id)
                document.sub_documents.extend(subs)

            docs_list.append(document)

        return docs_list
