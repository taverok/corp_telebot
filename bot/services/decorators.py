from functools import wraps

from telebot.types import Message

from bot.app import create_app
from bot.models.user import find_by_id


def push_app_context(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        app = create_app()
        app.app_context().push()
        return func(*args, **kwargs)

    return wrapped


def with_user(func):
    """ passes User to function params
    """
    @wraps(func)
    def wrapped(message: Message):
        app = create_app()
        app.app_context().push()
        user = find_by_id(message.from_user.id)
        return func(message, user=user)
    return wrapped
