from __future__ import annotations
from fastapi import APIRouter, Response, status
from app.core.config import get_setting


router = APIRouter(tags=["health"])
setting = get_setting()

@router.get("/health/live")
async def liveness() -> dict[str, str]:
    return {"status":"alive"}

