import click
import telebot
from flask.cli import with_appcontext
from flask import current_app as app
from telebot.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from bot.config import BOT_TOKEN
from bot.extensions import db
from bot.handlers.core import get_handler, list_routes, route_to_help
from bot.handlers.docs import _get_docs_list_response
from bot.models import Token, Document
from bot.models.user import Role, User, find_by_id
from bot.services.command import get_subcommand
from bot.services.decorators import push_app_context, with_user
from bot.services.fsm import StateMachine


bot: telebot.TeleBot = telebot.TeleBot(BOT_TOKEN)
stateMachine = StateMachine()


@click.command("start_bot")
@with_appcontext
def start_bot():
    with app.app_context():
        bot.polling(none_stop=True)


@bot.message_handler(commands=['help'])
@bot.edited_message_handler(commands=['help'])
@with_user
def help_command(message: Message, user: User):
    if not user:
        bot.send_message(message.chat.id, "Account needs activation")
        return

    routes = []
    routes.extend(list_routes(user.role, "/docs"))
    routes.extend(list_routes(user.role, "/user"))
    help_list = [route_to_help(r) for r in routes if r.handler.__doc__]

    if not user.is_active:
        help_list.insert(0, '/activate YOUR_TOKEN')

    bot.send_message(message.chat.id, "\n".join(help_list))


@bot.message_handler(commands=['start'])
@bot.edited_message_handler(commands=['start'])
def help_command(message: Message):
    text = '''Welcome to documentation bot. Here you will find useful information about the company. \
But, firstly you should activate your account with the command /activate YOUR_TOKEN.

/help for more information'''

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['docs'])
@bot.edited_message_handler(commands=['docs'])
@with_user
def docs_resource(message: Message, user: User):
    if not user:
        bot.send_message(message.chat.id, "Account needs activation")
        return

    subcommand = get_subcommand(message.text, default='list')

    handler_key = '/docs ' + subcommand
    handler = get_handler(handler_key, user.role)
    response = handler(message, user)

    bot.send_message(message.chat.id, str(response), reply_markup=response.reply_markup)
    stateMachine.set_state(message.from_user.id, 'last:' + handler_key)


@bot.message_handler(commands=['activate'])
@bot.edited_message_handler(commands=['activate'])
@push_app_context
def activate(message: Message):
    code = get_subcommand(message.text, default='')

    if not code or code.lower() != Token.get_current().code.lower():
        bot.send_message(message.chat.id, "Wrong activation code")
        return

    user = find_by_id(message.from_user.id) or User(telegram_id=message.from_user.id,
                                                    name=message.from_user.first_name,
                                                    surname=message.from_user.last_name,
                                                    role=Role.USER,
                                                    username=message.from_user.username
                                                    )
    if user.is_active:
        bot.send_message(message.chat.id, "Already activated")
        return

    user.is_active=True
    db.session.add(user)
    db.session.commit()

    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = KeyboardButton(text="Share your phone number", request_contact=True)
    keyboard.add(reg_button)

    bot.send_message(message.chat.id, "Successfully activated", reply_markup=keyboard)


@bot.message_handler(commands=['user'])
@bot.edited_message_handler(commands=['user'])
@with_user
def user_resource(message: Message, user: User):
    if not user:
        bot.send_message(message.chat.id, "Account needs activation")
        return

    subcommand = get_subcommand(message.text, default='list')

    handler = get_handler('/user '+subcommand, user.role)
    response = handler(message, user)

    bot.send_message(message.chat.id, str(response), reply_markup=response.reply_markup)
    stateMachine.set_state(message.from_user.id, 'last:docs/'+subcommand)


@bot.message_handler(func=lambda message: True, content_types=["text"])
@bot.edited_message_handler(func=lambda message: True, content_types=["text"])
@with_user
def text_message_dispatcher(message: Message, user: User):
    if not user:
        bot.send_message(message.chat.id, "Account needs activation")
        return

    user_state = stateMachine.get_state(message.from_user.id)
    handler = get_handler(user_state, user.role)

    response = handler(message, user)
    bot.send_message(message.chat.id, str(response))

    if not response.errors:
        stateMachine.remove_state(message.from_user.id)


@bot.message_handler(content_types=['contact'])
@with_user
@push_app_context
def contact_handler(message: Message, user: User):
    if not user:
        bot.send_message(message.chat.id, "Account needs activation")
        return

    user.phone = message.contact.phone_number
    db.session.commit()


@bot.callback_query_handler(func=lambda c: True)
@push_app_context
def docs_callback_dispatcher(c: CallbackQuery):
    doc = Document.find_by_id(int(c.data))
    response = _get_docs_list_response(doc.sub_documents, text=doc.content, no_subdocs_text=doc.content)

    bot.send_message(
        c.message.chat.id,
        str(response),
        reply_markup=response.reply_markup,
        parse_mode="HTML",
        disable_web_page_preview=True
    )

