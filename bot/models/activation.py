from datetime import datetime
from faker import Faker

from bot.extensions import db


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    @classmethod
    def gen_and_save(cls) -> 'Token':
        db.session.query(Token).delete()
        token = Token(code=generate())
        db.session.add(token)
        db.session.commit()

        return token

    @classmethod
    def get_current(cls) -> 'Token':
        return cls.query.one()


def generate() -> str:
    f = Faker()
    return f.password(special_chars=False, lower_case=False)


