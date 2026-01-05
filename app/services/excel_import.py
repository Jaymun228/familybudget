from pathlib import Path
from typing import Iterable, List

from openpyxl import load_workbook

from app.models import Transaction
from app.utils.constants import TransactionKind


def parse_transactions(path: Path) -> List[Transaction]:
    wb = load_workbook(path)
    parsed: list[Transaction] = []

    if "Повседневные" in wb.sheetnames:
        ws = wb["Повседневные"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue
            parsed.append(
                Transaction(
                    date=row[2],
                    title=row[3],
                    amount=row[6],
                    comment=row[7],
                    kind=TransactionKind.DAILY,
                )
            )
    if "Крупные" in wb.sheetnames:
        ws = wb["Крупные"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue
            parsed.append(
                Transaction(
                    date=row[1],
                    title=row[2],
                    amount=row[3],
                    kind=TransactionKind.BIG,
                )
            )
    if "Квартира" in wb.sheetnames:
        ws = wb["Квартира"]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue
            parsed.append(
                Transaction(
                    date=row[1],
                    title=row[3],
                    amount=row[4],
                    kind=TransactionKind.HOME,
                )
            )
    return parsed


def deduplicate(
    existing: Iterable[Transaction], imported: Iterable[Transaction]
) -> List[Transaction]:
    existing_keys = {
        (
            tx.kind,
            tx.date,
            (tx.title or "").strip().lower(),
            float(tx.amount),
            getattr(tx.category, "name", None),
            getattr(tx.subcategory, "name", None),
        )
        for tx in existing
    }
    result: list[Transaction] = []
    for tx in imported:
        key = (
            tx.kind,
            tx.date,
            (tx.title or "").strip().lower(),
            float(tx.amount),
            None,
            None,
        )
        if key in existing_keys:
            continue
        result.append(tx)
    return result
