import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from app.models import Category, Subcategory, Transaction
from app.services.excel_export import export_to_xlsx
from app.services.users import get_or_create_user
from app.utils.access import access_guard
from app.utils.keyboards import main_menu


async def _get_session(context: ContextTypes.DEFAULT_TYPE):
    factory = context.application.bot_data["session_factory"]
    return factory()


@access_guard
async def export_xlsx(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Готовлю экспорт...", reply_markup=main_menu())
    async with await _get_session(context) as session:
        user = await get_or_create_user(
            session, tg_id=update.effective_user.id, username=update.effective_user.username
        )
        tx_result = await session.execute(Transaction.__table__.select().where(Transaction.user_id == user.id))
        transactions = [Transaction(**row._mapping) for row in tx_result.fetchall()]
        cat_result = await session.execute(Category.__table__.select())
        categories = [Category(**row._mapping) for row in cat_result.fetchall()]
        sub_result = await session.execute(Subcategory.__table__.select())
        subcategories = [Subcategory(**row._mapping) for row in sub_result.fetchall()]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        export_to_xlsx(
            transactions=transactions,
            categories=categories,
            subcategories=subcategories,
            output_path=Path(tmp.name),
        )
        tmp_path = tmp.name

    await update.message.reply_document(open(tmp_path, "rb"), filename="budget1000.xlsx")
    await update.message.reply_text("Готово!", reply_markup=main_menu())


def register_export_handlers(app: Application) -> None:
    app.add_handler(MessageHandler(filters.Regex("^📤 Экспорт$"), export_xlsx))
