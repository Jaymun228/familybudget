import datetime as dt

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_user_id = Column(BigInteger, unique=True, nullable=False)
    is_owner = Column(Boolean, default=False, nullable=False)
    is_allowed = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
