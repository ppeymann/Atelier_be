from __future__ import annotations

import uuid

from app.repository.user import UserRepository
from app.models.user import User
from app.core.exceptions import UserNotFoundError
from app.schemas.user import UserCreate

class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository
        
    async def get_by_id(self, user_id: uuid.UUID) -> User:
        user = await self._repository.get_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundError()
        return user
    
    async def list_users(self, *, page: int, page_size: int) -> tuple[list[User], int]:
        return await self._repository.list_paginated(page=page, page_size=page_size)
    
    