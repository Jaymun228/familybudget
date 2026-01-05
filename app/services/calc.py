import datetime as dt
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, List

from app.models import Transaction
from app.utils.constants import TransactionType


@dataclass
class DashboardStats:
    last_expense_date: dt.date | None
    avg_per_day: Decimal
    daily_limit: Decimal
    status: str
    totals_by_type: dict[TransactionType, Decimal]
    top_categories: list[tuple[str, Decimal]]


def calculate_dashboard(
    transactions: Iterable[Transaction],
    *,
    month_start: dt.date,
    today: dt.date,
    daily_limit: Decimal,
) -> DashboardStats:
    totals_by_type: defaultdict[TransactionType, Decimal] = defaultdict(Decimal)
    totals_by_category: defaultdict[str, Decimal] = defaultdict(Decimal)
    last_date: dt.date | None = None

    for tx in transactions:
        totals_by_type[tx.type] += Decimal(tx.amount)
        if tx.category:
            totals_by_category[tx.category.name] += Decimal(tx.amount)
        if tx.tx_date and (last_date is None or tx.tx_date > last_date):
            last_date = tx.tx_date

    month_day = max((today - month_start).days + 1, 1)
    avg_per_day = (
        totals_by_type.get(TransactionType.DAILY, Decimal("0")) / Decimal(month_day)
    ).quantize(Decimal("0.01"))
    status = "ТРАНЖИРА" if avg_per_day > daily_limit else "В НОРМЕ"

    top_categories = sorted(
        totals_by_category.items(), key=lambda item: item[1], reverse=True
    )[:5]

    return DashboardStats(
        last_expense_date=last_date,
        avg_per_day=avg_per_day,
        daily_limit=daily_limit,
        status=status,
        totals_by_type=dict(totals_by_type),
        top_categories=top_categories,
    )
