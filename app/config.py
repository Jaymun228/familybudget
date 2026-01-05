import os
from dataclasses import dataclass, field
from typing import List, Optional

from dotenv import load_dotenv


@dataclass
class BotConfig:
    token: str
    owner_username: Optional[str]
    allowed_usernames: List[str] = field(default_factory=list)
    timezone: str = "Europe/Rome"


@dataclass
class DatabaseConfig:
    dsn: str
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20


@dataclass
class Settings:
    bot: BotConfig
    db: DatabaseConfig


def _split_list(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def load_settings() -> Settings:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set")

    db_dsn = os.getenv("DATABASE_DSN")
    if not db_dsn:
        raise RuntimeError("DATABASE_DSN is not set")

    return Settings(
        bot=BotConfig(
            token=bot_token,
            owner_username=os.getenv("OWNER_USERNAME"),
            allowed_usernames=_split_list(os.getenv("ALLOWED_USERNAMES")),
            timezone=os.getenv("TIMEZONE", "Europe/Rome"),
        ),
        db=DatabaseConfig(
            dsn=db_dsn,
            echo=os.getenv("DB_ECHO", "false").lower() == "true",
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
        ),
    )
