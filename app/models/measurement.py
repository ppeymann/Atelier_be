from __future__ import annotations

import uuid

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

class OrderMeasurement(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "order_measurements"
    
    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    
    order: Mapped["Order"] = relationship(back_populates="measurement")
    
    upper: Mapped["UpperMeasurement"] = relationship(
        back_populates="measurement",
        uselist=False,
        cascade="all, delete-orphan",
    )

    lower: Mapped["LowerMeasurement"] = relationship(
        back_populates="measurement",
        uselist=False,
        cascade="all, delete-orphan",
    )
    
    