from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    rows = [
<<<<<<< HEAD
        ["➕ Добавить расход", "📊 Дашборд"],
        ["📈 Отчёты", "📤 Экспорт"],
        ["📥 Импорт", "⚙️ Настройки"],
=======
        ["➕ Добавить расход", "➕ Крупная покупка"],
        ["➕ Квартира", "📊 Дашборд"],
        ["📈 Отчёты", "🧾 История"],
        ["📤 Экспорт", "⚙️ Настройки"],
>>>>>>> origin/main
        ["❓ Помощь"],
    ]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def back_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([["⬅️ Назад", "🏠 В меню"]], resize_keyboard=True)


<<<<<<< HEAD
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
=======
def date_choice_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Сегодня", callback_data="date_today")],
            [InlineKeyboardButton("Вчера", callback_data="date_yesterday")],
            [InlineKeyboardButton("📅 Выбрать дату", callback_data="date_pick")],
        ]
>>>>>>> origin/main
    )
