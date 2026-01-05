import datetime as dt

<<<<<<< HEAD
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
=======
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer
>>>>>>> origin/main

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
<<<<<<< HEAD
    tg_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False)
=======
    tg_user_id = Column(BigInteger, unique=True, nullable=False)
    is_owner = Column(Boolean, default=False, nullable=False)
    is_allowed = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
>>>>>>> origin/main
