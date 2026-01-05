import datetime as dt

from sqlalchemy import (
<<<<<<< HEAD
=======
    Boolean,
>>>>>>> origin/main
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

<<<<<<< HEAD
from app.utils.constants import TransactionKind
=======
from app.utils.constants import TransactionType
>>>>>>> origin/main
from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
<<<<<<< HEAD
        Index("ix_transactions_user_date", "user_id", "date"),
        Index("ix_transactions_user_kind_date", "user_id", "kind", "date"),
        Index("ix_transactions_user_category_date", "user_id", "category_id", "date"),
=======
        Index("ix_transactions_user_date", "user_id", "tx_date"),
        Index("ix_transactions_user_type_date", "user_id", "type", "tx_date"),
        Index("ix_transactions_user_category_date", "user_id", "category_id", "tx_date"),
>>>>>>> origin/main
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
<<<<<<< HEAD
    kind = Column(Enum(TransactionKind), nullable=False)
    date = Column(Date, nullable=False)
=======
    type = Column(Enum(TransactionType), nullable=False)
    tx_date = Column(Date, nullable=False)
>>>>>>> origin/main
    title = Column(String(256), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    comment = Column(String(512), nullable=True)
<<<<<<< HEAD
    created_at = Column(DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False)
=======
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow, nullable=False
    )
    is_deleted = Column(Boolean, default=False, nullable=False)
>>>>>>> origin/main

    category = relationship("Category")
    subcategory = relationship("Subcategory")
