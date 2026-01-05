from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    rows = [
        ["➕ Добавить расход", "📊 Дашборд"],
        ["📈 Отчёты", "📤 Экспорт"],
        ["📥 Импорт", "⚙️ Настройки"],
        ["❓ Помощь"],
    ]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def back_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([["⬅️ Назад", "🏠 В меню"]], resize_keyboard=True)


def date_choice_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [["Сегодня", "Вчера"], ["📅 Ввести дату вручную"], ["⬅️ Назад"]],
        resize_keyboard=True,
    )


def expense_kind_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            ["Повседневные", "Крупные"],
            ["Квартира"],
            ["⬅️ Назад"],
        ],
        resize_keyboard=True,
    )
