import json

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from bot.extensions import db
from bot.handlers.core import add_handler, list_routes, Route, route_to_help
from bot.models import Document
from bot.models.bot import BotResponse
from bot.models.user import Role, User
from bot.services.decorators import push_app_context


@push_app_context
def list_docs(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ list documents
    """
    docs = Document.get_all()
    keyboard = InlineKeyboardMarkup()

    for doc in docs:
        icon = "" if not doc.icon else doc.icon.decode()
        button = InlineKeyboardButton(text=f"{icon} {doc.title}", callback_data=f"/docs show {doc.id}")
        keyboard.add(button)

    return BotResponse("Список документов", reply_markup=keyboard)


def help_docs(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ this help
    """
    routes = list_routes(Role.ADMIN, "/docs")  # TODO: fix role
    help_list = [route_to_help(r) for r in routes if r.handler.__doc__]

    return BotResponse("\n".join(help_list))


def new_doc_help(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ create new document
    """
    content = '''Enter new document in json format:
    {
        "type": "document",
        "title": "my title",
        "icon": "icon_file_id (optional)",
        "content": "html content",
        "is_private": true
    }
    '''
    return BotResponse(content)


def edit_doc(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """edit document TODO
    """
    return BotResponse('edit')


@push_app_context
def new_doc_form(message: Message, user: User, *args, **kwargs) -> BotResponse:
    data = json.loads(message.text)
    required_keys = ('title', 'content')

    if len(data.keys() & ('title', 'content')) < len(required_keys):
        return BotResponse(f"All required fields must be set {required_keys}")

    # TODO: call recursive if subdocuments exist
    document = Document(
        title=data.get('title'),
        icon=data.get('icon', "").encode(),
        content=data.get('content'),
        user_id=message.from_user.id
    )
    db.session.add(document)
    db.session.commit()

    return BotResponse('OK')


add_handler('/docs help', help_docs, Role.USER)
add_handler('/docs list', list_docs, Role.USER)
add_handler('/docs new', new_doc_help, Role.ADMIN)
add_handler('last:/docs new', new_doc_help, Role.ADMIN, False)
add_handler('/docs edit', edit_doc, Role.ADMIN)
