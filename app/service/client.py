from __future__ import annotations

import uuid

from app.repository.client import ClientRepository
from app.models.client import Client
from app.core.exceptions import UserNotFoundError, AlreadyExistError
from app.schemas.client import ClientCreate, ClientUpdate
from app.core.exceptions import PhoneAlreadyCreateClientError
from app.core.config import get_setting
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_setting()


class ClientService:
    def __init__(self, repo: ClientRepository) -> None:
        self._repo: ClientRepository = repo
    
    async def get_by_id(self, client_id: uuid.UUID) -> Client:
        client: Client | None = await self._repo.get_by_id(client_id)
        if client is None:
            raise UserNotFoundError()
        return client
    
    async def list_clients(self, *, page: int, page_size: int) -> tuple[list[Client], int]:
        return await self._repo.list_paginated(page=page, page_size=page_size)
    
    async def create(self, payload: ClientCreate, user_id: uuid.UUID) -> Client:
        exist = await self._repo.get_by_phone(payload.phone)
        if exist is not None:
            raise PhoneAlreadyCreateClientError()
        client:Client = Client(
            phone=payload.phone,
            email=payload.email,
            first_name = payload.first_name,
            last_name=payload.last_name,
            birth_day = payload.birth_day,
            city=payload.city,
            preferred_style=payload.preferred_style,
            notes=payload.notes,
            user_id=user_id
        )
        
        client = await self._repo.create(client)
        logger.info("client_created", client_id=str(client.id), phone=client.phone)
        return client
    
    async def delete(self, client_id: uuid.UUID) -> None:
        client: Client = await self._repo.get_by_id(client_id)
        if client is None:
            raise UserNotFoundError()
        
        await self._repo.delete(client)
        
    async def update(self, client_id: uuid.UUID, payload: ClientUpdate) -> Client:
        client: Client | None = await self._repo.get_by_id(client_id)
        if client is None:
            raise UserNotFoundError()
        update_data = payload.model_dump(exclude_unset=True)
        phone = update_data.get("phone")
        if phone is not None and phone != client.phone:
            exist = await self._repo.get_by_phone(phone)
            if exec is not None:
                raise AlreadyExistError()
        
        client = await self._repo.update(client, **update_data)
        logger.info("client_update", client_id=str(client_id))
        return client
    
        
        
    