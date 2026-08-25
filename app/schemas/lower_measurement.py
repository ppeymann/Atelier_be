from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LowerMeasurementBase(BaseModel):
    hip: float | None = None
    thigh: float | None = None
    knee: float | None = None
    calf: float | None = None
    pants_lenght: float | None = None
    inseam: float | None = None


class LowerMeasurementCreate(LowerMeasurementBase):
    pass


class LowerMeasurementUpdate(BaseModel):
    hip: float | None = None
    thigh: float | None = None
    knee: float | None = None
    calf: float | None = None
    pants_lenght: float | None = None
    inseam: float | None = None


class LowerMeasurementRead(LowerMeasurementBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    measurement_id: uuid.UUID
    created_at: datetime
    updated_at: datetime