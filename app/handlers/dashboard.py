import datetime as dt
from decimal import Decimal

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from app.models import Transaction
from app.services.calc import calculate_dashboard
from app.services.settings import load_avg_flags, load_daily_limit
from app.services.users import get_or_create_user
from app.utils.access import access_guard
from app.utils.constants import TransactionKind
from app.utils.keyboards import main_menu


async def _get_session(context: ContextTypes.DEFAULT_TYPE):
    factory = context.application.bot_data["session_factory"]
    return factory()


@access_guard
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async with await _get_session(context) as session:
        user = await get_or_create_user(
            session, tg_id=update.effective_user.id, username=update.effective_user.username
        )
        today = dt.date.today()
        month_start = today.replace(day=1)
        result = await session.execute(
            Transaction.__table__.select().where(
                Transaction.user_id == user.id,
                Transaction.date >= month_start,
                Transaction.kind.in_(
                    [TransactionKind.DAILY, TransactionKind.BIG, TransactionKind.HOME]
                ),
            )
        )
        tx_rows = result.fetchall()
        txs = [Transaction(**row._mapping) for row in tx_rows]
        limit = await load_daily_limit(session, user)
        include_big, include_home = await load_avg_flags(session, user)
        stats = calculate_dashboard(
            txs,
            month_start=month_start,
            today=today,
            daily_limit=limit or Decimal("2000"),
            include_big=include_big,
            include_home=include_home,
        )

    lines = [
        "📊 Дашборд",
        f"Последние расходы внесены: {stats.last_expense_date or '—'}",
        f"Средний расход за текущий месяц: {stats.avg_per_day} ",
        f"Лимит расхода в день: {stats.daily_limit}",
        f"Статус: {stats.status}",
        "",
        "Траты за месяц:",
        f"• Повседневные: {stats.totals_by_kind.get(TransactionKind.DAILY, Decimal('0'))}",
        f"• Крупные: {stats.totals_by_kind.get(TransactionKind.BIG, Decimal('0'))}",
        f"• Квартира: {stats.totals_by_kind.get(TransactionKind.HOME, Decimal('0'))}",
    ]
    if stats.top_categories:
        lines.append("\nТОП категорий:")
        for name, value in stats.top_categories[:5]:
            lines.append(f"- {name}: {value}")
    await update.message.reply_text("\n".join(lines), reply_markup=main_menu())


def register_dashboard_handlers(app: Application) -> None:
    app.add_handler(MessageHandler(filters.Regex("^📊 Дашборд$"), dashboard))
