from __future__ import annotations

import uuid

from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

class LowerMeasurement(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "lower_measurements"
    
    measurement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("order_measurements.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    hip: Mapped[float | None]
    thigh: Mapped[float | None]
    knee: Mapped[float | None]
    calf: Mapped[float | None]
    pants_lenght: Mapped[float | None]
    inseam: Mapped[float | None]
    
    measurement: Mapped["OrderMeasurement"] = relationship(back_populates="lower")
