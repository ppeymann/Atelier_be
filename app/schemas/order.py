from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Status(StrEnum):
    received = "RECEIVED"
    cutting = "CUTTING"
    sewing = "SEWING"
    finishing = "FINISHING"
    ready = "READY"

class OrderBase(BaseModel):
    customer_nots: str = Field(..., max_length=255)
    price: float = 0.00
    delivery: date | None = None
    deposit: float = Field(..., ge=0, le=100)
    status: Status = Status.received
    clothing_type: str = Field(default="Suit", max_length=255)
    fabric_type: str | None = Field(default=None, max_length=255)
    fabric_color: str | None = Field(default=None, max_length=255)
    lining: str | None = Field(default=None, max_length=255)


class OrderCreate(OrderBase):
    client_id: uuid.UUID


class OrderUpdate(BaseModel):
    customer_nots: str | None = Field(default=None, max_length=255)
    price: float | None = None
    delivery: date | None = None
    deposit: float | None = Field(default=None, ge=0, le=100)
    status: Status | None = None
    clothing_type: str | None = Field(default=None, max_length=255)
    fabric_type: str | None = Field(default=None, max_length=255)
    fabric_color: str | None = Field(default=None, max_length=255)
    lining: str | None = Field(default=None, max_length=255)
    client_id: uuid.UUID | None = None


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    client_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
