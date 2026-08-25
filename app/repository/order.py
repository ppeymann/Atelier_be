from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order, Status
from app.models.measurement import OrderMeasurement
from app.schemas.order import OrderCreate, OrderUpdate

class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        
    async def create(self, order: Order) -> Order:
        self._session.add(order)
        await self._session.flush()
        return order
    
    async def get(self, order_id: uuid.UUID) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.measurement).selectinload(OrderMeasurement.upper),
                selectinload(Order.measurement).selectinload(OrderMeasurement.lower),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
    async def list(
        self, 
        *, 
        client_id: uuid.UUID | None = None,
        page:int,
        page_size:int) -> Sequence[Order]:
        stmt = select(Order).where(Order.client_id == client_id).options(
            selectinload(Order.measurement).selectinload(OrderMeasurement.upper),
            selectinload(Order.measurement).selectinload(OrderMeasurement.lower),
        ).order_by(Order.created_at.desc()).limit(page_size).offset((page - 1) * page_size)
        
        result = await self._session.execute(stmt)
        return result.scalars().all()
    
    async def count(self, *, client_id: uuid.UUID | None = None) -> int:
        stmt = select(func.count()).select_from(Order)
        if client_id is not None:
            stmt = stmt.where(Order.client_id == client_id)
        result = await self._session.execute(stmt)
        return result.scalar_one()
    
    async def update(self, order_id: uuid.UUID, data: Order, **fields: object) -> Order | None:
        order = await self.get(order_id)
        if order is None:
            return None

        
        for key, value in fields.items():
            setattr(order, key, value)
        await self._session.flush()
        return order
    
    async def delete(self, order_id: uuid.UUID) -> bool:
        order = await self.get(order_id)
        if order is None:
            return False
        await self._session.delete(order)
        await self._session.flush()
        return True
    
        
        
    
        