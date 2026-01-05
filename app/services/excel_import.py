from pathlib import Path
from typing import Iterable, List

from openpyxl import load_workbook

from app.models import Transaction
from app.utils.constants import TransactionType


def parse_transactions(path: Path) -> List[Transaction]:
    wb = load_workbook(path)
    mapping = {
        "Повседневные": TransactionType.DAILY,
        "Крупные": TransactionType.BIG,
        "Квартира": TransactionType.APARTMENT,
    }
    parsed: list[Transaction] = []
    for sheet_name, tx_type in mapping.items():
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue
            tx = Transaction(
                tx_date=row[2],
                title=row[3],
                amount=row[6],
                comment=row[7],
                type=tx_type,
            )
            parsed.append(tx)
    return parsed


def deduplicate(
    existing: Iterable[Transaction], imported: Iterable[Transaction]
) -> List[Transaction]:
    existing_keys = {
        (tx.type, tx.tx_date, (tx.title or "").strip().lower(), float(tx.amount))
        for tx in existing
    }
    result: list[Transaction] = []
    for tx in imported:
        key = (tx.type, tx.tx_date, (tx.title or "").strip().lower(), float(tx.amount))
        if key in existing_keys:
            continue
        result.append(tx)
    return result
