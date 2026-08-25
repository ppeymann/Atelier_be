from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.upper_measurement import UpperMeasurementRead, UpperMeasurementCreate
from app.schemas.lower_measurement import LowerMeasurementRead, LowerMeasurementCreate



class OrderMeasurementBase(BaseModel):
    pass  

class OrderMeasurementCreate(OrderMeasurementBase):
    order_id: uuid.UUID
    upper: UpperMeasurementCreate | None = None
    lower: LowerMeasurementCreate | None = None



class OrderMeasurementUpdate(BaseModel):
    order_id: uuid.UUID | None = None
    upper: UpperMeasurementCreate | None = None
    lower: LowerMeasurementCreate | None = None



class OrderMeasurementRead(OrderMeasurementBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    upper: UpperMeasurementRead | None = None
    lower: LowerMeasurementRead | None = None