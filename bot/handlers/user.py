from telebot.types import Message

from bot.extensions import db
from bot.handlers.core import add_handler, list_routes, route_to_help
from bot.models import Token
from bot.models.bot import BotResponse
from bot.models.user import Role, User, get_all_users
from bot.services.decorators import push_app_context

PREFIX = "/user"


def help_users(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ help for user resource
    """
    routes = list_routes(user.role, PREFIX)
    help_list = [route_to_help(r) for r in routes if r.handler.__doc__]

    return BotResponse("\n".join(help_list))


def list_users(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ list all active users
    """
    response_list = [u.to_table_format(with_id=user.is_admin()) for u in get_all_users()]
    return BotResponse('\n'.join(response_list))


@push_app_context
def flush_activation(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ deactivates user with passed id
    """
    tokens = message.text.split(" ")
    if len(tokens) < 3:
        return BotResponse("pass in arguments user_id (or -1 for all)")

    _id = int(tokens[2])
    user = User.query.filter_by(role=Role.USER, telegram_id=_id).first()
    user.is_active = False

    db.session.commit()

    return BotResponse(f"user {user.telegram_id} deactivated")


@push_app_context
def new_token(message: Message, user: User, *args, **kwargs):
    """ generates new activation Token and removes old
    """
    token = Token.gen_and_save()

    return BotResponse(f"New token is {token.code}")


@push_app_context
def show_token(message: Message, user: User, *args, **kwargs):
    """ prints current activation code
    """
    token = Token.get_current()

    return BotResponse(token.code if token else "No token found, you should generate it")


add_handler(PREFIX + ' help', help_users, Role.USER)
add_handler(PREFIX + ' list', list_users, Role.USER)
add_handler(PREFIX + ' flush', flush_activation, Role.ADMIN)
add_handler(PREFIX + ' new_token', new_token, Role.ADMIN)
add_handler(PREFIX + ' show_token', show_token, Role.ADMIN)
