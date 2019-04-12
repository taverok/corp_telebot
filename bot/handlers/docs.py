import json

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from bot.app import create_app
from bot.extensions import db
from bot.models import Document
from bot.models.bot import BotResponse


def list_docs():
    app = create_app()
    app.app_context().push()

    docs = Document.get_all()
    keyboard = InlineKeyboardMarkup()

    for doc in docs:
        icon = "" if not doc.icon else doc.icon.decode()
        button = InlineKeyboardButton(text=f"{icon} {doc.title}", callback_data=f"/docs show {doc.id}")
        keyboard.add(button)

    return BotResponse("Список документов", reply_markup=keyboard)


def help_docs() -> BotResponse:
    return BotResponse('help docs')


def new_doc_help() -> BotResponse:
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


def edit_doc(message) -> BotResponse:
    """edit document
    """
    return BotResponse('edit')


docs_handler_map = {
    'edit': edit_doc,
    'new': new_doc_help,
    'help': list_docs,
    'list': list_docs,
}


def new_doc_form(message: Message) -> BotResponse:
    app = create_app()
    app.app_context().push()

    data = json.loads(message.text)
    required_keys = ('title', 'content')

    if len(data.keys() & ('title', 'content')) < len(required_keys):
        return BotResponse(f"All required fields must be set {required_keys}")

    document = Document(
        title=data.get('title'),
        icon=data.get('icon', "").encode(),
        content=data.get('content'),
        user_id=message.from_user.id
    )
    db.session.add(document)
    db.session.commit()

    return BotResponse('OK')


docs_state_map = {
    'docs.new': new_doc_form,
}