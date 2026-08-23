from __future__ import annotations

from fastapi import APIRouter, Depends, status

from typing import Annotated

from app.schemas.client import ClientRead, ClientCreate
from app.service.client import ClientService
from app.api.dependencies import get_client_service, get_current_user
from app.models.client import Client

router: APIRouter = APIRouter(prefix="/clients", tags=["clients"])

@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_client(
    payload: ClientCreate,
    client_service: Annotated[ClientService, Depends(get_client_service)],
    
) -> ClientRead:
    client: Client = await client_service.create(payload)
    return ClientRead.model_validate(client)

