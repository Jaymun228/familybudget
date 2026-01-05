from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

<<<<<<< HEAD
from app.utils.access import access_guard
from app.utils.keyboards import main_menu


@access_guard
=======
from app.utils.keyboards import main_menu


>>>>>>> origin/main
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_first = update.effective_user.first_name or "друг"
    await update.message.reply_text(
        (
            "Привет! Я бот Budget1000. Помогаю вести семейный бюджет по методике "
            "1000 дней расходов.\n\nИспользуйте кнопки для начала работы."
        ),
        reply_markup=main_menu(),
    )
    context.application.logger.info("User %s executed /start", user_first)


<<<<<<< HEAD
@access_guard
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Основные возможности:\n"
        "• Добавляйте расходы кнопками меню.\n"
        "• Смотрите дашборд и отчёты.\n"
        "• Экспортируйте и импортируйте данные в XLSX.\n"
=======
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Основные возможности:\n"
        "• Добавляйте расходы и доходы кнопками меню.\n"
        "• Смотрите дашборд и отчёты.\n"
        "• Экспортируйте данные в XLSX или CSV.\n"
>>>>>>> origin/main
        "• Управляйте категориями и лимитами через ⚙️ Настройки.",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu(),
    )


<<<<<<< HEAD
@access_guard
=======
>>>>>>> origin/main
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Используйте кнопки меню, чтобы продолжить.", reply_markup=main_menu()
    )


def register_menu_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))
