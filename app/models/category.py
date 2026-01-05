import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

<<<<<<< HEAD
from app.utils.constants import CategoryKind
=======
from app.utils.constants import CategoryScope
>>>>>>> origin/main
from .base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
<<<<<<< HEAD
    kind = Column(Enum(CategoryKind), nullable=False, default=CategoryKind.DAILY)
    name = Column(String(128), nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=dt.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=dt.datetime.utcnow,
        onupdate=dt.datetime.utcnow,
        nullable=False,
    )

    subcategories = relationship("Subcategory", back_populates="category", cascade="all,delete")
=======
    scope = Column(Enum(CategoryScope), nullable=False)
    name = Column(String(128), nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow, nullable=False
    )

    subcategories = relationship("Subcategory", back_populates="category")
>>>>>>> origin/main
