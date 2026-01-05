import datetime as dt

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.utils.constants import SettingScope
from .base import Base


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    scope = Column(Enum(SettingScope), nullable=False, default=SettingScope.GLOBAL)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    key = Column(String(128), nullable=False)
    value = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False)

    user = relationship("User")
