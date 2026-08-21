from __future__ import annotations



from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    balance: Mapped[int] = mapped_column(nullable=False, default=0)
    
    
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} phone={self.phone}>"