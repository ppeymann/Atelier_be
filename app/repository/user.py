from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        
    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return await self._session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def list_paginated(self, *, page: int, page_size: int) -> tuple[list[User], int]:
        count_result = await self._session.execute(select(func.count()).select_from(User))
        total = count_result.scalar_one()

        result = await self._session.execute(
            select(User)
            .order_by(User.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(result.scalars().all()), total
    
    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()  # populate defaults (id, created_at) without committing
        return user

    async def update(self, user: User, **fields: object) -> User:
        for key, value in fields.items():
            setattr(user, key, value)
        await self._session.flush()
        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.flush()