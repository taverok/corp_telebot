import json
from typing import List

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from bot.extensions import db
from bot.handlers.core import add_handler, list_routes, route_to_help
from bot.models import Document
from bot.models.bot import BotResponse
from bot.models.user import Role, User
from bot.services.decorators import push_app_context


def _get_docs_list_response(docs: List[Document], text="Content", no_docs_text="No content", parent: Document = None, debug=False) -> BotResponse:
    text = text if docs else no_docs_text
    keyboard = InlineKeyboardMarkup()

    for doc in docs:
        title = f"{doc.get_icon()} {doc.title: <100}..."
        # if parent:
        #     title += f"{parent.get_icon()} {parent.title}\n"

        if debug:
            title += f"{{id: {doc.id} }}"
        button = InlineKeyboardButton(text=title, callback_data=f"{doc.id}")
        keyboard.add(button)

    return BotResponse(text, reply_markup=keyboard)


@push_app_context
def list_docs(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ list documents
    """
    return _get_docs_list_response(Document.find_all_by_parent_id(parent_id=None))


@push_app_context
def list_debug_docs(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ list documents
    """
    return _get_docs_list_response(Document.find_all_by_parent_id(parent_id=None), debug=True)


def help_docs(message: Message, user: User, *args, **kwargs) -> BotResponse:
    """ help for document resource
    """
    routes = list_routes(user.role, "/docs")
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


@push_app_context
def delete_doc(message: Message, user: User, *args, **kwargs) -> BotResponse:
    tokens = message.text.split(" ")
    if len(tokens) < 3:
        return BotResponse("pass in arguments user_id (or -1 for all)")
    _id = int(tokens[2])
    doc = Document.find_by_id(_id)
    doc.is_visible = False
    db.session.commit()

    return BotResponse(f'id: {_id} deleted')


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
add_handler('/docs list_debug', list_debug_docs, Role.ADMIN)
add_handler('/docs new', new_doc_help, Role.ADMIN)
add_handler('last:/docs new', new_doc_form, Role.ADMIN, False)
add_handler('/docs delete', delete_doc, Role.ADMIN)
