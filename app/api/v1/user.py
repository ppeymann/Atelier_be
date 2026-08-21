from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_user_service
from app.api.dependencies import CurrentUser
from app.schemas.user import UserRead, UserListItem
from app.schemas.common import PaginatedResponse
from app.service.user import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
async def get_profile(current_user:CurrentUser) -> UserRead:
    return UserRead.model_validate(current_user)

@router.get("/{user_id}", response_model=UserRead)
async def get_(user_id: uuid.UUID, user_service: Annotated[UserService, Depends(get_user_service)]):
    user = await user_service.get_by_id(user_id)
    return UserRead.model_validate(user)
