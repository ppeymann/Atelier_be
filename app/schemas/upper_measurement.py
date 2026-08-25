from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict



class UpperMeasurementBase(BaseModel):
    neck: float | None = None
    chest: float | None = None
    waist: float | None = None
    shoulder_width: float | None = None
    arm_circumference: float | None = None
    sleeve_length: float | None = None


class UpperMeasurementCreate(UpperMeasurementBase):
    pass


class UpperMeasurementUpdate(BaseModel):
    neck: float | None = None
    chest: float | None = None
    waist: float | None = None
    shoulder_width: float | None = None
    arm_circumference: float | None = None
    sleeve_length: float | None = None


class UpperMeasurementRead(UpperMeasurementBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    measurement_id: uuid.UUID
    created_at: datetime
    updated_at: datetime