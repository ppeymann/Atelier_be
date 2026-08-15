from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field



class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=255)
    last_name: str = Field(min_length=3, max_length=255)
    phone: str = Field(min_length=11, max_length=11, pattern=r"^09\d{9}$")
    
class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Must contain at least 8 characters"
    )
    
    re_password: str = Field(
        min_length=8,
        max_length=128,
        description="Must contain at least 8 characters"
    )
    
class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime