from __future__ import annotations

import uuid

from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

class UpperMeasurement(Base, TimestampMixin, UUIDPrimaryKeyMixin):
    __tablename__ = "upper_measurements"
    
    measurement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("order_measurements.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    neck: Mapped[float | None]
    chest: Mapped[float | None]
    waist: Mapped[float | None]
    shoulder_width: Mapped[float | None]
    arm_circumference: Mapped[float | None]
    sleeve_length: Mapped[float | None]
    
    measurement: Mapped["OrderMeasurement"] = relationship(back_populates="upper")
