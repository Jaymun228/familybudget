from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt

from app.models import Transaction
<<<<<<< HEAD
from app.utils.constants import TransactionKind
=======
from app.utils.constants import TransactionType
>>>>>>> origin/main


def line_spending_by_day(transactions: Iterable[Transaction], output: Path) -> Path:
    totals: dict[str, float] = {}
    for tx in transactions:
<<<<<<< HEAD
        if tx.kind != TransactionKind.DAILY:
            continue
        key = tx.date.strftime("%d")
=======
        if tx.type != TransactionType.DAILY:
            continue
        key = tx.tx_date.strftime("%d")
>>>>>>> origin/main
        totals[key] = totals.get(key, 0) + float(tx.amount)
    xs = sorted(totals.keys())
    ys = [totals[key] for key in xs]
    plt.figure(figsize=(6, 3))
    plt.plot(xs, ys, marker="o")
    plt.title("Расходы по дням")
    plt.xlabel("День")
    plt.ylabel("Сумма")
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    return output
