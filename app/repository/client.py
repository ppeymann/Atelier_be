from __future__ import annotations

import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client

class ClientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        
    async def get_by_id(self, client_id: uuid.UUID) -> Client | None:
        return await self._session.get(Client, client_id)
    
    async def list_paginated(self, *, page:int, page_size:int) -> tuple[list[Client], int]:
        count_result = await self._session.execute(select(func.count()).select_from(Client))
        total = count_result.scalar_one()
        
        result = await self._session.execute(
            select(Client)
            .order_by(Client.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        
        return list(result.scalars().all()), total
    
    async def create(self, client: Client) -> Client:
        self._session.add(client)
        await self._session.flush()
        return client
    
    async def update(self, client: Client, **field: object) -> Client:
        for key,value in field.items():
            setattr(client, key, value)
        await self._session.flush()
        return client
        
    async def delete(self, client: Client) -> None:
        await self._session.delete(client)
        await self._session.flush()