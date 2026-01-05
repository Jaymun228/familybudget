from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    rows = [
        ["➕ Добавить расход", "➕ Крупная покупка"],
        ["➕ Квартира", "📊 Дашборд"],
        ["📈 Отчёты", "🧾 История"],
        ["📤 Экспорт", "⚙️ Настройки"],
        ["❓ Помощь"],
    ]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def back_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([["⬅️ Назад", "🏠 В меню"]], resize_keyboard=True)


def date_choice_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Сегодня", callback_data="date_today")],
            [InlineKeyboardButton("Вчера", callback_data="date_yesterday")],
            [InlineKeyboardButton("📅 Выбрать дату", callback_data="date_pick")],
        ]
    )
