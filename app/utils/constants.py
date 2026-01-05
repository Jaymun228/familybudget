import enum


class CategoryScope(str, enum.Enum):
    DAILY = "DAILY"
    APARTMENT = "APARTMENT"


class TransactionType(str, enum.Enum):
    DAILY = "DAILY"
    BIG = "BIG"
    APARTMENT = "APARTMENT"


class AverageMode(str, enum.Enum):
    DAILY_ONLY = "DAILY_ONLY"
    DAILY_AND_APARTMENT = "DAILY_AND_APARTMENT"
    ALL = "ALL"
