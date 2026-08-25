from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Sequence

from app.models.order import Order, Status
from app.repository.order import OrderRepository
from app.schemas.order import OrderCreate, OrderUpdate,OrderPage, OrderRead
from app.core.exceptions import NotFoundError, PageMustBiggerThan, PageSizeNotValid

class OrderService:
    def __init__(self, repository: OrderRepository):
        self._repo = repository
        
    async def create_order(self, payload: OrderCreate) -> Order:
        order = Order(**payload.model_dump())
        return await self._repo.create(order)
    
    async def get_order(self, order_id: uuid.UUID) -> Order:
        order = await self._repo.get(order_id)
        if order is None:
            raise NotFoundError()
        return order
    
    async def list(
        self,
        *,
        client_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
    ) -> OrderPage:
        if page < 1:
            raise PageMustBiggerThan()
        if page_size < 1 or page_size > 100:
            raise PageSizeNotValid()
        
        orders = await self._repo.list(client_id, page, page_size)
        total = await self._repo.count(client_id)
        
        return OrderPage(
            items=[OrderRead.model_validate(order) for order in orders],
            page=page,
            page_size=page_size,
            total=total,
        )
        
    async def update_order(self, order_id: uuid.UUID, payload: OrderUpdate) -> Order:
        field = payload.model_dump(exclude_unset=True)
        order = await self._repo.update(order_id, Order, **field)
        if order is None:
            raise NotFoundError()
        return order
    
    async def delete_order(self, order_id: uuid) -> None:
        deleted: bool = await self._repo.delete(order_id)
        if not deleted:
            raise NotFoundError()
        