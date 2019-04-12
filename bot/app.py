from flask import Flask

from bot.extensions import db, migrate


def create_app(testing=False, cli=False):
    app = Flask('bot')

    configure_logger(app)

    configure_app(app, testing)
    configure_extensions(app, cli)
    register_commands(app)

    return app


def configure_app(app, testing=False):
    app.config.from_object('bot.config')

    if testing is True:
        app.config.from_object('bot.configtest')
    else:
        app.config.from_envvar("BOT_CONFIG", silent=True)


def configure_extensions(app, cli):
    db.init_app(app)
    migrate.init_app(app, db)


def configure_logger(app):
    import logging
    from logging.handlers import RotatingFileHandler

    handler = RotatingFileHandler('app.log', maxBytes=10**8, backupCount=3)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('[%(asctime)s] - %(filename)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s'))
    app.logger.addHandler(handler)


def register_commands(app):
    from bot.tasks.bot import start_bot

    app.cli.add_command(start_bot)
