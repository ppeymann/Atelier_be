from __future__ import annotations
from redis.asyncio import ConnectionPool, Redis
from app.core.config import get_setting
from typing import Any
import json


_pool: ConnectionPool | None = None
_client: Redis | None = None

def get_redis_client() -> Redis:
    global _pool, _client
    if _client is None:
        settings = get_setting()
        _pool = ConnectionPool.from_url(
            str(settings.REDIS_URL), decode_responses=True, max_connections=50
        )
        _client = Redis(connection_pool=_pool)
    return _client

async def close_redis_client() -> None:
    global _client, _pool
    if _client is not None:
        await _client.aclose()
        _client = None
    if _pool is not None:
        await _pool.disconnect()
        _pool = None

async def check_redis_health() -> bool:
    try:
        return bool(await get_redis_client().ping())
    except Exception:
        return False

class RedisService:
    def __init__(self, client:Redis | None = None) -> None:
        self._client = client or get_redis_client()
        
    # --- Generic cache ops --------------------------------------------
    async def get_json(self, key: str) -> Any | None:
        raw = await self._client.get(key)
        return json.loads(raw) if raw is not None else None
    
    async def set_json(self, key: str, value: Any, *, ttl_seconds: int | None = None) -> None:
        await self._client.set(key, json.dump(value), ex=ttl_seconds)
        
    async def delete(self, key: str) -> None:
        await self._client.delete(key)
        
    # --- Access-token denylist (for immediate logout) --------------------
    async def denylist_access_token(self, jti:str, ttl_seconds: int) -> None:
        await self._client.set(f"denylist:access:{jti}", "1", ex=ttl_seconds)
        
    async def is_access_token_denylisted(self, jti:str) -> bool:
        return bool(await self._client.exists(f"denylist:access:{jti}"))
    
    
    # --- Login brute-force protection -----------------------------------
    async def register_failed_login(self, email:str, ttl_seconds: int = 900) -> int:
        key = f"login_failures:{email}"
        count = await self._client.incr(key)
        if count == 1:
            await self._client.expire(key, ttl_seconds)
        return count
    
    async def clrear_failed_logins(self, email: str) -> None:
        await self._client.delete(f"login_failures:{email}")
    
    async def get_failed_login_count(self, email:str) -> None:
        value = await self._client.get(f"login_failures:{email}")
        return int(value) if value else 0
    