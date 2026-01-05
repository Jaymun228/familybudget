import enum


<<<<<<< HEAD
class CategoryKind(str, enum.Enum):
    DAILY = "daily"


class TransactionKind(str, enum.Enum):
    DAILY = "daily"
    BIG = "big"
    HOME = "home"


class SettingScope(str, enum.Enum):
    GLOBAL = "global"
    USER = "user"
=======
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
>>>>>>> origin/main
