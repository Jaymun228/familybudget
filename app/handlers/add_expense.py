import datetime as dt
from decimal import Decimal
from typing import Any, Dict, Optional

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.models import Category, Subcategory, Transaction
from app.services.seed import ensure_seed_categories
from app.services.users import get_or_create_user
from app.utils.access import access_guard
from app.utils.constants import TransactionKind
from app.utils.keyboards import back_menu, date_choice_keyboard, expense_kind_keyboard, main_menu

(
    CHOOSING_KIND,
    CHOOSING_DATE,
    DAILY_TITLE,
    DAILY_CATEGORY,
    DAILY_SUBCATEGORY,
    DAILY_AMOUNT,
    DAILY_COMMENT,
    CONFIRM,
) = range(8)


def _parse_amount(text: str) -> Optional[Decimal]:
    clean = text.replace(" ", "").replace(",", ".")
    try:
        value = Decimal(clean)
    except Exception:
        return None
    if value <= 0:
        return None
    return value.quantize(Decimal("0.01"))


def _category_keyboard(categories: list[Category]) -> ReplyKeyboardMarkup:
    names = [c.name for c in sorted(categories, key=lambda c: c.sort_order)]
    rows = [names[i : i + 2] for i in range(0, len(names), 2)]
    rows.append(["⬅️ Назад"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


def _subcategory_keyboard(subcategories: list[Subcategory]) -> ReplyKeyboardMarkup:
    names = [s.name for s in sorted(subcategories, key=lambda s: s.sort_order)]
    rows = [names[i : i + 2] for i in range(0, len(names), 2)]
    rows.append(["- без подкатегории -"])
    rows.append(["⬅️ Назад"])
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)


@access_guard
async def entry(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Выберите тип расхода", reply_markup=expense_kind_keyboard())
    return CHOOSING_KIND


async def _get_session(context: CallbackContext):
    factory = context.application.bot_data["session_factory"]
    return factory()


@access_guard
async def choose_kind(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    kind_map = {
        "Повседневные": TransactionKind.DAILY,
        "Крупные": TransactionKind.BIG,
        "Квартира": TransactionKind.HOME,
    }
    if text not in kind_map:
        await update.message.reply_text("Выберите один из вариантов", reply_markup=expense_kind_keyboard())
        return CHOOSING_KIND
    context.user_data["kind"] = kind_map[text]
    await update.message.reply_text("Выберите дату", reply_markup=back_menu())
    await update.message.reply_text("Дата:", reply_markup=date_choice_keyboard())
    return CHOOSING_DATE


@access_guard
async def choose_date(update: Update, context: CallbackContext) -> int:
    data = update.message.text if update.message else ""
    if data == "⬅️ Назад":
        await update.effective_message.reply_text("Выберите тип расхода", reply_markup=expense_kind_keyboard())
        return CHOOSING_KIND
    today = dt.date.today()
    if data in ("Сегодня",):
        context.user_data["date"] = today
    elif data in ("Вчера",):
        context.user_data["date"] = today - dt.timedelta(days=1)
    elif data == "📅 Ввести дату вручную":
        await update.effective_message.reply_text("Введите дату в формате ДД.ММ.ГГГГ")
        return CHOOSING_DATE
    else:
        try:
            context.user_data["date"] = dt.datetime.strptime(data.strip(), "%d.%m.%Y").date()
        except Exception:
            await update.effective_message.reply_text("Введите дату в формате ДД.ММ.ГГГГ или выберите кнопку.")
            return CHOOSING_DATE

    kind: TransactionKind = context.user_data["kind"]
    if kind == TransactionKind.DAILY:
        await update.effective_message.reply_text("Наименование покупки:", reply_markup=back_menu())
        return DAILY_TITLE
    if kind == TransactionKind.BIG:
        await update.effective_message.reply_text("Что купили? (текст)", reply_markup=back_menu())
        return DAILY_TITLE
    if kind == TransactionKind.HOME:
        await update.effective_message.reply_text(
            "Категория квартиры (Ипотека/ЖКХ/Все для дома/Другое):", reply_markup=back_menu()
        )
        return DAILY_CATEGORY
    return ConversationHandler.END


@access_guard
async def daily_title(update: Update, context: CallbackContext) -> int:
    context.user_data["title"] = update.message.text.strip()
    kind: TransactionKind = context.user_data["kind"]
    if kind == TransactionKind.DAILY:
        async with await _get_session(context) as session:
            await ensure_seed_categories(session)
            result = await session.execute(
                Category.__table__.select().where(Category.is_active == True).order_by(Category.sort_order)  # noqa: E712
            )
            categories = [Category(**row._mapping) for row in result.fetchall()]
        context.user_data["categories"] = categories
        await update.message.reply_text("Выберите категорию:", reply_markup=_category_keyboard(categories))
        return DAILY_CATEGORY
    if kind == TransactionKind.BIG:
        await update.message.reply_text("Сумма:", reply_markup=back_menu())
        return DAILY_AMOUNT
    if kind == TransactionKind.HOME:
        await update.message.reply_text("Описание (опционально, можно пропустить '-'):", reply_markup=back_menu())
        return DAILY_SUBCATEGORY
    return ConversationHandler.END


@access_guard
async def daily_category(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == "⬅️ Назад":
        await update.message.reply_text("Выберите тип расхода", reply_markup=expense_kind_keyboard())
        return CHOOSING_KIND
    kind: TransactionKind = context.user_data["kind"]
    if kind == TransactionKind.HOME:
        context.user_data["category_name"] = text
        await update.message.reply_text("Описание (опционально, можно '-'):", reply_markup=back_menu())
        return DAILY_SUBCATEGORY
    categories: list[Category] = context.user_data.get("categories", [])
    match = next((c for c in categories if c.name == text), None)
    if not match:
        await update.message.reply_text("Выберите из списка.", reply_markup=_category_keyboard(categories))
        return DAILY_CATEGORY
    context.user_data["category_id"] = match.id
    async with await _get_session(context) as session:
        subs_res = await session.execute(
            Subcategory.__table__.select()
            .where(Subcategory.category_id == match.id, Subcategory.is_active == True)  # noqa: E712
            .order_by(Subcategory.sort_order)
        )
        subs = [Subcategory(**row._mapping) for row in subs_res.fetchall()]
    if subs:
        context.user_data["subcategories"] = subs
        await update.message.reply_text("Подкатегория:", reply_markup=_subcategory_keyboard(subs))
        return DAILY_SUBCATEGORY
    context.user_data["subcategory_id"] = None
    await update.message.reply_text("Сумма:", reply_markup=back_menu())
    return DAILY_AMOUNT


@access_guard
async def daily_subcategory(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text == "⬅️ Назад":
        return await daily_category(update, context)
    if text == "- без подкатегории -" or text == "-":
        context.user_data["subcategory_id"] = None
    elif "subcategories" in context.user_data:
        subs: list[Subcategory] = context.user_data["subcategories"]
        match = next((s for s in subs if s.name == text), None)
        if not match:
            await update.message.reply_text("Выберите из списка", reply_markup=_subcategory_keyboard(subs))
            return DAILY_SUBCATEGORY
        context.user_data["subcategory_id"] = match.id
    else:
        context.user_data["title"] = text
    await update.message.reply_text("Сумма:", reply_markup=back_menu())
    return DAILY_AMOUNT


@access_guard
async def daily_amount(update: Update, context: CallbackContext) -> int:
    amount = _parse_amount(update.message.text)
    if amount is None:
        await update.message.reply_text("Введите сумму числом (например 1234.56).")
        return DAILY_AMOUNT
    context.user_data["amount"] = amount
    await update.message.reply_text("Комментарий (или '-' чтобы пропустить):", reply_markup=back_menu())
    return DAILY_COMMENT


@access_guard
async def daily_comment(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text and text.strip() != "-":
        context.user_data["comment"] = text.strip()
    else:
        context.user_data["comment"] = None
    return await confirm(update, context)


async def confirm(update: Update, context: CallbackContext) -> int:
    data = context.user_data
    kind: TransactionKind = data["kind"]
    date_str = data["date"].strftime("%d.%m.%Y")
    parts = [
        f"Дата: {date_str}",
        f"Тип: {kind.value}",
        f"Наименование: {data.get('title')}",
        f"Сумма: {data.get('amount')}",
    ]
    if data.get("category_name"):
        parts.append(f"Категория: {data['category_name']}")
    if data.get("comment"):
        parts.append(f"Комментарий: {data['comment']}")
    await update.message.reply_text("\n".join(parts) + "\n\nСохраняю...", reply_markup=main_menu())

    async with await _get_session(context) as session:
        user = await get_or_create_user(
            session,
            tg_id=update.effective_user.id,
            username=update.effective_user.username,
        )
        comment = data.get("comment")
        if kind == TransactionKind.HOME and data.get("category_name"):
            prefix = f"Категория: {data['category_name']}"
            comment = f"{prefix}. {comment}" if comment else prefix
        tx = Transaction(
            user_id=user.id,
            kind=kind,
            date=data["date"],
            title=data.get("title"),
            category_id=data.get("category_id"),
            subcategory_id=data.get("subcategory_id"),
            amount=data["amount"],
            comment=comment,
        )
        session.add(tx)
        await session.commit()

    await update.message.reply_text("✅ Сохранено", reply_markup=main_menu())
    context.user_data.clear()
    return ConversationHandler.END


@access_guard
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Отмена. Возвращаю в меню.", reply_markup=main_menu())
    context.user_data.clear()
    return ConversationHandler.END


def register_add_expense_handlers(app: Application) -> None:
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^➕ Добавить расход$"), entry)],
        states={
            CHOOSING_KIND: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_kind)],
            CHOOSING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_date)],
            DAILY_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_title)],
            DAILY_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_category)],
            DAILY_SUBCATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_subcategory)],
            DAILY_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_amount)],
            DAILY_COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, daily_comment)],
        },
        fallbacks=[CommandHandler("cancel", cancel), MessageHandler(filters.Regex("^(⬅️ Назад|🏠 В меню)$"), cancel)],
        name="add_expense",
        persistent=False,
    )
    app.add_handler(conv)
