import datetime as dt

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from .base import Base


class Setting(Base):
    __tablename__ = "settings"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    daily_limit = Column(Numeric(12, 2), default=2000.00, nullable=False)
    currency = Column(String(8), default="RUB", nullable=False)
    timezone = Column(String(64), default="Europe/Rome", nullable=False)
    week_start = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow, nullable=False
    )

    user = relationship("User")
