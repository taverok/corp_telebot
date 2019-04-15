from telebot.types import Message

from bot.extensions import db
from bot.handlers.core import add_handler, list_routes, Route, route_to_help
from bot.models.bot import BotResponse
from bot.models.user import Role, User
from bot.services.decorators import push_app_context

PREFIX = "/user"


def help_users(message: Message, user: User) -> BotResponse:
    """ this help
    """
    routes = list_routes(Role.ADMIN, PREFIX)
    help_list = [route_to_help(r) for r in routes if r.handler.__doc__]

    return BotResponse("\n".join(help_list))


def list_users(message: Message, user: User) -> BotResponse:
    """ list all active users
    """
    return BotResponse("Not yet implemented")


@push_app_context
def flush_activation(message: Message, user: User) -> BotResponse:
    """ makes all users not activated and invalidates current activation code.
    Required params: [user telegram_id | -1 for all]
    """
    tokens = message.text.split(" ")
    if len(tokens) < 3:
        return BotResponse("pass user id or -1 for all")

    _id = int(tokens[2])
    query = User.query.filter_by(role=Role.USER)

    if _id != -1:
        query = query.filter_by(telegram_id=_id)

    users = query.all()
    for user in users:
        user.is_active = False

    db.session.commit()

    return BotResponse(f"{len(users)} user deactivated")


add_handler(PREFIX + ' help', help_users, Role.USER)
add_handler(PREFIX + ' list', list_users, Role.USER)
add_handler(PREFIX + ' flush', flush_activation, Role.ADMIN)
