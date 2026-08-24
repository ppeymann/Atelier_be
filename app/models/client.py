import uuid
from datetime import date

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Client(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "clients"

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(11), unique=True, index=True, nullable=False)
    
    birth_day: Mapped[date | None] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    preferred_style: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_vip: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relations
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship(back_populates="clients")
    orders: Mapped[list["Order"]] = relationship(
        back_populates="client",
        cascade="all, delete-orphan"
    )