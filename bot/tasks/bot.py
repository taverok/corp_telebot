import click
import jsonpickle
import telebot
from flask.cli import with_appcontext
from flask import current_app as app
from telebot.types import Message, CallbackQuery

from bot.config import BOT_TOKEN
from bot.extensions import db
from bot.handlers.core import get_handler
from bot.models.bot import BotResponse
from bot.models.user import Role, User, find_by_id
from bot.services.command import get_subcommand
from bot.services.decorators import push_app_context, with_user
from bot.services.fsm import StateMachine


bot: telebot.TeleBot = telebot.TeleBot(BOT_TOKEN)
stateMachine = StateMachine()
ACTIVATION_CODE = "aaa"


@click.command("start_bot")
@with_appcontext
def start_bot():
    with app.app_context():
        bot.polling(none_stop=True)


@bot.message_handler(commands=['docs'])
@bot.edited_message_handler(commands=['docs'])
@with_user
def docs_dispatcher(message: Message, user: User):
    if not user:
        bot.send_message(message.chat.id, "Account needs activation")
        return

    subcommand = get_subcommand(message.text, default='list')

    handler = get_handler('/docs '+subcommand, user.role)
    response = handler()

    bot.send_message(message.chat.id, response.content, reply_markup=response.reply_markup)
    stateMachine.set_state(message.from_user.id, 'last:docs/'+subcommand)


@bot.message_handler(commands=['activate'])
@bot.edited_message_handler(commands=['activate'])
@push_app_context
def activate(message: Message):
    code = get_subcommand(message.text, default='')

    if code != ACTIVATION_CODE:
        bot.send_message(message.chat.id, "Wrong activation code")

    user = find_by_id(message.from_user.id) or User(telegram_id=message.from_user.id,
                                                    name=message.from_user.first_name,
                                                    surname=message.from_user.last_name,
                                                    role=Role.USER
                                                    )
    if user.is_active:
        bot.send_message(message.chat.id, "Already activated")
        return

    user.is_active=True
    db.session.add(user)
    db.session.commit()

    bot.send_message(message.chat.id, "Successfully activated")


@bot.message_handler(commands=['user'])
@bot.edited_message_handler(commands=['user'])
@with_user
def user_dispatcher(message: Message, user: User):
    if not user:
        bot.send_message(message.chat.id, "Account needs activation")
        return

    subcommand = get_subcommand(message.text, default='list')

    handler = get_handler('/user '+subcommand, user.role)
    response = handler(message, user)

    bot.send_message(message.chat.id, response.content, reply_markup=response.reply_markup)
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

    response = handler(message) if handler else BotResponse(f"no handler found: user state {user_state}")

    bot.send_message(message.chat.id, response.content)

    stateMachine.remove_state(message.from_user.id)


@bot.callback_query_handler(func=lambda c: True)
@push_app_context
def docs_callback_dispatcher(c: CallbackQuery):
    bot.send_message(c.message.chat.id, type(c))

