import datetime as dt

from sqlalchemy import (
    Boolean,
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

from app.utils.constants import TransactionType
from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_user_date", "user_id", "tx_date"),
        Index("ix_transactions_user_type_date", "user_id", "type", "tx_date"),
        Index("ix_transactions_user_category_date", "user_id", "category_id", "tx_date"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    tx_date = Column(Date, nullable=False)
    title = Column(String(256), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    comment = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow, nullable=False
    )
    is_deleted = Column(Boolean, default=False, nullable=False)

    category = relationship("Category")
    subcategory = relationship("Subcategory")
