import enum


class CategoryKind(str, enum.Enum):
    DAILY = "daily"


class TransactionKind(str, enum.Enum):
    DAILY = "daily"
    BIG = "big"
    HOME = "home"


class SettingScope(str, enum.Enum):
    GLOBAL = "global"
    USER = "user"
