from typing import Callable

from telegram import Update
from telegram.ext import ContextTypes


def is_allowed_user(update: Update, allowed_usernames: list[str], owner_username: str | None) -> bool:
    user = update.effective_user
    if not user or not user.username:
        return False
    username = user.username.lstrip("@")
    if owner_username and username.lower() == owner_username.lower():
        return True
    return username.lower() in [u.lower() for u in allowed_usernames]


def access_guard(handler: Callable):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        settings = context.application.bot_data.get("settings")
        if not settings:
            return
        allowed = is_allowed_user(update, settings.bot.allowed_usernames, settings.bot.owner_username)
        if not allowed:
            if update.effective_message:
                await update.effective_message.reply_text("Нет доступа")
            return
        return await handler(update, context)

    return wrapper
