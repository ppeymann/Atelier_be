from __future__ import annotations

import uuid
from datetime import datetime, date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=255)
    last_name: str = Field(min_length=3, max_length=255)
    phone: str = Field(min_length=11, max_length=11, pattern=r"^09\d{9}$")
    birth_day: date | None = None
    city: str = Field(min_length=3, max_length=255)
    preferred_style: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=255)
    is_vip: bool = False


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = Field(default=None, min_length=3, max_length=255)
    last_name: str | None = Field(default=None, min_length=3, max_length=255)
    phone: str | None = Field(default=None, min_length=11, max_length=11, pattern=r"^09\d{9}$")
    birth_day: date | None = None
    city: str | None = Field(default=None, min_length=3, max_length=255)
    preferred_style: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=255)
    is_vip: bool | None = None


class ClientRead(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
class ClientListItem(ClientRead):
    pass

class PaginatedResponse(BaseModel):
    items: list[ClientListItem]
    total: int
    page: int
    page_size:int