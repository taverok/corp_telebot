import json

import click
import telebot
from flask.cli import with_appcontext
from telebot.types import Message

from bot.config import BOT_TOKEN
from bot.handlers.docs import docs_handler_map, docs_state_map
from bot.models.bot import BotResponse
from bot.services.command import get_subcommand
from bot.services.fsm import StateMachine

bot: telebot.TeleBot = telebot.TeleBot(BOT_TOKEN)
stateMachine = StateMachine()


@click.command("start_bot")
@with_appcontext
def start_bot():
    bot.polling(none_stop=True)


@bot.message_handler(commands=['docs'])
@bot.edited_message_handler(commands=['docs'])
def docs_dispatcher(message: Message):
    subcommand = get_subcommand(message.text, default='list')

    handler = docs_handler_map.get(subcommand, 'help')
    response = handler()

    bot.send_message(message.chat.id, response.content, reply_markup=response.reply_markup)
    stateMachine.set_state(message.from_user.idm, 'docs.'+subcommand)


@bot.message_handler(func=lambda message: True, content_types=["text"])
@bot.edited_message_handler(func=lambda message: True, content_types=["text"])
def text_message_dispatcher(message: Message):
    user_state = stateMachine.get_state(message.from_user.id)

    handler = docs_state_map.get(user_state)

    response = handler(message) if handler else BotResponse(f"no handler found: user state {user_state}")

    bot.send_message(message.chat.id, response.content)

    stateMachine.remove_state(message.from_user.id)


@bot.callback_query_handler(func=lambda c: True)
def docs_callback_dispatcher(message: Message):
    pass
