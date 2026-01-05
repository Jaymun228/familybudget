import datetime as dt
from decimal import Decimal

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CallbackContext, ConversationHandler, MessageHandler, filters

from app.models import Transaction
from app.utils.access import access_guard
from app.utils.constants import TransactionKind
from app.utils.keyboards import main_menu

CHOOSE_PERIOD = 1
CUSTOM_FROM = 2
CUSTOM_TO = 3


async def _get_session(context: CallbackContext):
    factory = context.application.bot_data["session_factory"]
    return factory()


def _period_dates(choice: str) -> tuple[dt.date, dt.date]:
    today = dt.date.today()
    if choice == "Текущий месяц":
        start = today.replace(day=1)
        end = today
    elif choice == "Прошлый месяц":
        first_this = today.replace(day=1)
        last_prev = first_this - dt.timedelta(days=1)
        start = last_prev.replace(day=1)
        end = last_prev
    elif choice == "Последние 7 дней":
        end = today
        start = today - dt.timedelta(days=6)
    elif choice == "Последние 30 дней":
        end = today
        start = today - dt.timedelta(days=29)
    else:
        start = end = today
    return start, end


@access_guard
async def start_reports(update: Update, context: CallbackContext) -> int:
    options = ReplyKeyboardMarkup(
        [["Текущий месяц", "Прошлый месяц"], ["Последние 7 дней", "Последние 30 дней"], ["Произвольный период"]],
        resize_keyboard=True,
    )
    await update.message.reply_text("Выберите период отчёта:", reply_markup=options)
    return CHOOSE_PERIOD


@access_guard
async def choose_period(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == "Произвольный период":
        await update.message.reply_text("Введите дату начала в формате ДД.ММ.ГГГГ")
        return CUSTOM_FROM
    start, end = _period_dates(text)
    await _render_report(update, context, start, end)
    return ConversationHandler.END


@access_guard
async def custom_from(update: Update, context: CallbackContext) -> int:
    try:
        context.user_data["from_date"] = dt.datetime.strptime(update.message.text.strip(), "%d.%m.%Y").date()
    except Exception:
        await update.message.reply_text("Формат даты: ДД.ММ.ГГГГ")
        return CUSTOM_FROM
    await update.message.reply_text("Введите дату конца в формате ДД.ММ.ГГГГ")
    return CUSTOM_TO


@access_guard
async def custom_to(update: Update, context: CallbackContext) -> int:
    try:
        to_date = dt.datetime.strptime(update.message.text.strip(), "%d.%m.%Y").date()
    except Exception:
        await update.message.reply_text("Формат даты: ДД.ММ.ГГГГ")
        return CUSTOM_TO
    from_date = context.user_data.pop("from_date")
    await _render_report(update, context, from_date, to_date)
    return ConversationHandler.END


async def _render_report(update: Update, context: CallbackContext, start: dt.date, end: dt.date) -> None:
    async with await _get_session(context) as session:
        user = update.effective_user
        from app.services.users import get_or_create_user  # local import to avoid cycle

        db_user = await get_or_create_user(session, tg_id=user.id, username=user.username)
        result = await session.execute(
            Transaction.__table__.select().where(
                Transaction.user_id == db_user.id,
                Transaction.date >= start,
                Transaction.date <= end,
            )
        )
        txs = [Transaction(**row._mapping) for row in result.fetchall()]
    totals = {
        TransactionKind.DAILY: Decimal("0"),
        TransactionKind.BIG: Decimal("0"),
        TransactionKind.HOME: Decimal("0"),
    }
    for tx in txs:
        totals[tx.kind] += Decimal(tx.amount)
    lines = [
        f"Отчёт {start.strftime('%d.%m.%Y')} — {end.strftime('%d.%m.%Y')}",
        f"Повседневные: {totals[TransactionKind.DAILY]}",
        f"Крупные: {totals[TransactionKind.BIG]}",
        f"Квартира: {totals[TransactionKind.HOME]}",
        "",
    ]
    await update.message.reply_text("\n".join(lines), reply_markup=main_menu())


@access_guard
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Отчёт отменён.", reply_markup=main_menu())
    return ConversationHandler.END


def register_report_handlers(app: Application) -> None:
    from telegram import ReplyKeyboardMarkup

    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📈 Отчёты$"), start_reports)],
        states={
            CHOOSE_PERIOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_period)],
            CUSTOM_FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, custom_from)],
            CUSTOM_TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, custom_to)],
        },
        fallbacks=[MessageHandler(filters.Regex("^(⬅️ Назад|🏠 В меню)$"), cancel)],
    )
    app.add_handler(conv)
