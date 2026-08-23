from __future__ import annotations

from fastapi import APIRouter, Depends, status

import uuid

from typing import Annotated

from app.schemas.client import ClientRead, ClientCreate, ClientListItem, PaginatedResponse,ClientUpdate
from app.service.client import ClientService
from app.api.dependencies import CurrentUser
from app.api.dependencies import get_client_service, get_current_user
from app.models.client import Client

router: APIRouter = APIRouter(prefix="/clients", tags=["clients"])

@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_client(
    payload: ClientCreate,
    client_service: Annotated[ClientService, Depends(get_client_service)],
    current_user: CurrentUser
    
) -> ClientRead:
    client: Client = await client_service.create(payload, current_user.id)
    return ClientRead.model_validate(client)

@router.get("/all", response_model=PaginatedResponse, dependencies=[Depends(get_current_user)])
async def get_clients(page: int, page_size:int ,client_service: Annotated[ClientService, Depends(get_client_service)]):
    clients, total = await client_service.list_clients(page=page, page_size=page_size)
    return PaginatedResponse(
        items=clients,
        total=total,
        page=page,
        page_size=page_size
    )
    
@router.get("/{client_id}", response_model=ClientRead, status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def get_by_id(client_id: uuid.UUID, client_service: Annotated[ClientService, Depends(get_client_service)]):
    client: Client = await client_service.get_by_id(client_id)
    return ClientRead.model_validate(client)

@router.patch("/{client_id}", dependencies=[Depends(get_current_user)])
async def update_client(
    client_id: uuid.UUID,
    payload: ClientUpdate,
    client_service: Annotated[ClientService, Depends(get_client_service)]
        ):
    client: Client = await client_service.update(client_id=client_id, payload=payload)
    return ClientRead.model_validate(client)

@router.delete("/{client_id}", dependencies=[Depends(get_current_user)])
async def delete_client(
    client_id: uuid.UUID,
    client_service: Annotated[ClientService, Depends(get_client_service)]
):
    await client_service.delete(client_id)
    return {
        "client_id": client_id
    }