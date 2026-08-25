from __future__ import annotations

import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import TimestampMixin, UUIDPrimaryKeyMixin, Base
from sqlalchemy import String, Boolean, ForeignKey,CheckConstraint, Enum as SAEnum
from enum import StrEnum
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.client import Client
    from app.models.measurement import OrderMeasurement

class Status(StrEnum):
    received = "RECEIVED"
    cutting = "CUTTING"
    sewing = "SEWING"
    finishing = "FINISHING"
    ready = "READY"
    

class Order(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "orders"
    
    customer_nots: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(nullable=False, default=0.00)
    delivery: Mapped[date | None] = mapped_column(nullable=True)
    
    
    deposit: Mapped[float] = mapped_column(nullable=False)
    __table_args__ = (
        CheckConstraint("deposit >= 0 AND deposit <= 100", name="check_deposit_range"),
    )
    
    status: Mapped[Status] = mapped_column(
        SAEnum(Status, name="order_status"),
        default=Status.received,
        nullable=False
    )
    
    clothing_type: Mapped[str] = mapped_column(String(255), nullable=False, default="Suit")
    fabric_type:  Mapped[str | None] = mapped_column(String(255))
    fabric_color:  Mapped[str | None] = mapped_column(String(255))
    lining:  Mapped[str | None] = mapped_column(String(255))
    
    # Relations
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    client: Mapped["Client"] = relationship(back_populates="orders")
    measurement: Mapped["OrderMeasurement"] = relationship(
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )
    