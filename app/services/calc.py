import datetime as dt
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
<<<<<<< HEAD
from typing import Iterable

from app.models import Transaction
from app.utils.constants import TransactionKind
=======
from typing import Iterable, List

from app.models import Transaction
from app.utils.constants import TransactionType
>>>>>>> origin/main


@dataclass
class DashboardStats:
    last_expense_date: dt.date | None
    avg_per_day: Decimal
    daily_limit: Decimal
    status: str
<<<<<<< HEAD
    totals_by_kind: dict[TransactionKind, Decimal]
=======
    totals_by_type: dict[TransactionType, Decimal]
>>>>>>> origin/main
    top_categories: list[tuple[str, Decimal]]


def calculate_dashboard(
    transactions: Iterable[Transaction],
    *,
    month_start: dt.date,
    today: dt.date,
    daily_limit: Decimal,
<<<<<<< HEAD
    include_big: bool = False,
    include_home: bool = False,
) -> DashboardStats:
    totals_by_kind: defaultdict[TransactionKind, Decimal] = defaultdict(Decimal)
=======
) -> DashboardStats:
    totals_by_type: defaultdict[TransactionType, Decimal] = defaultdict(Decimal)
>>>>>>> origin/main
    totals_by_category: defaultdict[str, Decimal] = defaultdict(Decimal)
    last_date: dt.date | None = None

    for tx in transactions:
<<<<<<< HEAD
        totals_by_kind[tx.kind] += Decimal(tx.amount)
        if tx.category:
            totals_by_category[tx.category.name] += Decimal(tx.amount)
        if tx.date and (last_date is None or tx.date > last_date):
            last_date = tx.date

    month_day = max((today - month_start).days + 1, 1)
    avg_base = Decimal("0")
    avg_base += totals_by_kind.get(TransactionKind.DAILY, Decimal("0"))
    if include_big:
        avg_base += totals_by_kind.get(TransactionKind.BIG, Decimal("0"))
    if include_home:
        avg_base += totals_by_kind.get(TransactionKind.HOME, Decimal("0"))
    avg_per_day = (avg_base / Decimal(month_day)).quantize(Decimal("0.01"))
=======
        totals_by_type[tx.type] += Decimal(tx.amount)
        if tx.category:
            totals_by_category[tx.category.name] += Decimal(tx.amount)
        if tx.tx_date and (last_date is None or tx.tx_date > last_date):
            last_date = tx.tx_date

    month_day = max((today - month_start).days + 1, 1)
    avg_per_day = (
        totals_by_type.get(TransactionType.DAILY, Decimal("0")) / Decimal(month_day)
    ).quantize(Decimal("0.01"))
>>>>>>> origin/main
    status = "ТРАНЖИРА" if avg_per_day > daily_limit else "В НОРМЕ"

    top_categories = sorted(
        totals_by_category.items(), key=lambda item: item[1], reverse=True
<<<<<<< HEAD
    )[:10]
=======
    )[:5]
>>>>>>> origin/main

    return DashboardStats(
        last_expense_date=last_date,
        avg_per_day=avg_per_day,
        daily_limit=daily_limit,
        status=status,
<<<<<<< HEAD
        totals_by_kind=dict(totals_by_kind),
=======
        totals_by_type=dict(totals_by_type),
>>>>>>> origin/main
        top_categories=top_categories,
    )
