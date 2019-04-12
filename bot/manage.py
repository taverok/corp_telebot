import click
from flask.cli import FlaskGroup

from bot.app import create_app


def create_bot(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_bot)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    pass


if __name__ == "__main__":
    cli()
