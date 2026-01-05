from telegram.ext import Application

from .menu import register_menu_handlers


def register_handlers(app: Application) -> None:
    register_menu_handlers(app)
