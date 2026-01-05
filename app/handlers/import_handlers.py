import tempfile
from pathlib import Path

from telegram import Document, Update
from telegram.ext import Application, CallbackContext, ConversationHandler, MessageHandler, filters

from app.models import Transaction
from app.services.excel_import import deduplicate, parse_transactions
from app.services.users import get_or_create_user
from app.utils.access import access_guard
from app.utils.keyboards import main_menu

WAITING_FILE = 1


async def _get_session(context: CallbackContext):
    factory = context.application.bot_data["session_factory"]
    return factory()


@access_guard
async def start_import(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Пришлите XLSX файл из шаблона Т—Ж.", reply_markup=main_menu())
    return WAITING_FILE


@access_guard
async def receive_file(update: Update, context: CallbackContext) -> int:
    doc: Document = update.message.document
    if not doc or not doc.file_name.endswith(".xlsx"):
        await update.message.reply_text("Нужен файл .xlsx")
        return WAITING_FILE

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        file_path = Path(tmp.name)
    new_file = await doc.get_file()
    await new_file.download_to_drive(custom_path=str(file_path))

    imported = parse_transactions(file_path)
    async with await _get_session(context) as session:
        user = await get_or_create_user(
            session, tg_id=update.effective_user.id, username=update.effective_user.username
        )
        existing_result = await session.execute(
            Transaction.__table__.select().where(Transaction.user_id == user.id)
        )
        existing = [Transaction(**row._mapping) for row in existing_result.fetchall()]
        to_insert = deduplicate(existing, imported)
        for tx in to_insert:
            tx.user_id = user.id
            session.add(tx)
        await session.commit()

    await update.message.reply_text(f"Импорт завершён. Добавлено записей: {len(to_insert)}", reply_markup=main_menu())
    return ConversationHandler.END


@access_guard
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Отмена импорта.", reply_markup=main_menu())
    return ConversationHandler.END


def register_import_handlers(app: Application) -> None:
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📥 Импорт$"), start_import)],
        states={
            WAITING_FILE: [MessageHandler(filters.Document.ALL, receive_file)],
        },
        fallbacks=[MessageHandler(filters.Regex("^(⬅️ Назад|🏠 В меню)$"), cancel)],
    )
    app.add_handler(conv)
