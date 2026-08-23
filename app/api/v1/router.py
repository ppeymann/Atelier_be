from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import auth, user, client

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(client.router)

