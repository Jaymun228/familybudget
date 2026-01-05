import datetime as dt

<<<<<<< HEAD
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.utils.constants import SettingScope
=======
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

>>>>>>> origin/main
from .base import Base


class Setting(Base):
    __tablename__ = "settings"

<<<<<<< HEAD
    id = Column(Integer, primary_key=True)
    scope = Column(Enum(SettingScope), nullable=False, default=SettingScope.GLOBAL)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    key = Column(String(128), nullable=False)
    value = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False)
=======
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    daily_limit = Column(Numeric(12, 2), default=2000.00, nullable=False)
    currency = Column(String(8), default="RUB", nullable=False)
    timezone = Column(String(64), default="Europe/Rome", nullable=False)
    week_start = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow, nullable=False
    )
>>>>>>> origin/main

    user = relationship("User")
