import json
from typing import List

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from bot.extensions import db
from bot.handlers.core import add_handler, list_routes, Route, route_to_help
from bot.models import Document
from bot.models.bot import BotResponse
from bot.models.user import Role, User
from bot.services.decorators import push_app_context


def _get_docs_list_response(subdocs: List[Document], text="Content", no_subdocs_text="No content") -> BotResponse:
    text = text if subdocs else no_subdocs_text
    keyboard = InlineKeyboardMarkup()

    for doc in subdocs:
        icon = "" if not doc.icon else doc.icon.decode()
        button = InlineKeyboardButton(text=f"{icon} {doc.title}", callback_data=f"{doc.id}")
        keyboard.add(button)

    return BotResponse(text, reply_markup=keyboard)


@push_app_context
def list_docs(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ list documents
    """
    return _get_docs_list_response(Document.find_all_by_parent_id(parent_id=None))


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
        "title": "Document title",
        "icon": "📃",
        "content": "HTML content",
        "sub": [
            {
                "title": "Sub documents title",
                "icon": "➡️",
                "content": "HTML content"
            }
        ]
    }
    '''
    return BotResponse(content)


def delete_doc(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """deletes document TODO
    """
    return BotResponse('edit')


@push_app_context
def new_doc_form(message: Message, user: User, *args, **kwargs) -> BotResponse:
    try:
        data = json.loads(message.text)
    except:
        return BotResponse("json is invalid")

    docs = Document.from_json(data, message.from_user.id)

    db.session.add_all(docs)
    db.session.commit()

    return BotResponse('OK')


add_handler('/docs help', help_docs, Role.USER)
add_handler('/docs list', list_docs, Role.USER)
add_handler('/docs new', new_doc_help, Role.ADMIN)
add_handler('last:/docs new', new_doc_form, Role.ADMIN, False)
add_handler('/docs delete', delete_doc, Role.ADMIN)
