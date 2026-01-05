from decimal import Decimal
from typing import Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Setting, User
from app.utils.constants import SettingScope

DEFAULTS = {
    "daily_limit": "2000",
    "include_big_in_avg": "false",
    "include_home_in_avg": "false",
}


async def get_setting(session: AsyncSession, key: str, user: User | None = None) -> str | None:
    stmt = select(Setting.value).where(
        Setting.scope == (SettingScope.USER if user else SettingScope.GLOBAL),
        Setting.key == key,
    )
    if user:
        stmt = stmt.where(Setting.user_id == user.id)
    result = await session.execute(stmt)
    val = result.scalar_one_or_none()
    if val is not None:
        return val
    return DEFAULTS.get(key)


async def upsert_setting(session: AsyncSession, key: str, value: str, user: User | None = None) -> None:
    stmt = select(Setting).where(
        Setting.scope == (SettingScope.USER if user else SettingScope.GLOBAL),
        Setting.key == key,
    )
    if user:
        stmt = stmt.where(Setting.user_id == user.id)
    result = await session.execute(stmt)
    setting = result.scalar_one_or_none()
    if setting:
        setting.value = value
    else:
        setting = Setting(
            scope=SettingScope.USER if user else SettingScope.GLOBAL,
            user_id=user.id if user else None,
            key=key,
            value=value,
        )
        session.add(setting)
    await session.commit()


async def load_avg_flags(session: AsyncSession, user: User | None) -> Tuple[bool, bool]:
    big_raw = await get_setting(session, "include_big_in_avg", user)
    home_raw = await get_setting(session, "include_home_in_avg", user)
    return (big_raw or "false").lower() == "true", (home_raw or "false").lower() == "true"


async def load_daily_limit(session: AsyncSession, user: User | None) -> Decimal:
    raw = await get_setting(session, "daily_limit", user) or DEFAULTS["daily_limit"]
    try:
        return Decimal(str(raw))
    except Exception:
        return Decimal(DEFAULTS["daily_limit"])
