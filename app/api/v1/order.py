from __future__ import annotations

import uuid

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_order_service, get_current_user, CurrentUser
from app.models.order import Status
from app.schemas.order import OrderCreate, OrderPage, OrderRead, OrderUpdate
from app.service.order import NotFoundError, OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED, dependencies=Depends(get_current_user))
async def create_order(
    payload: OrderCreate,
    service: Annotated[OrderService, Depends(get_order_service)]
) -> OrderRead:
    order = await service.create_order(payload)
    return OrderRead.model_validate(order)

@router.get("/{order_id}", response_model=OrderRead, dependencies=Depends(get_current_user))
async def get_order(order_id: uuid.UUID, service: Annotated[OrderService, Depends(get_order_service)]) -> OrderRead:
    try:
        order = await service.get_order(order_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return OrderRead.model_validate(order)

# @router.get("", response_model=OrderPage, dependencies=Depends(get_current_user))
# async def list_order()

