from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import TokenType, decode_token
from app.auth.service import AuthService
from app.db.session import get_db
from app.core.exceptions import InactiveUserError, InsufficientPermissionsError, InvalidTokenError
from app.models.user import User
from app.repository.user import UserRepository
from app.service.user import UserService
from app.utils.redis import RedisService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=True)

def get_user_repository(session: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(session)

def get_redis_service() -> RedisService:
    return RedisService()

def get_auth_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    redis: Annotated[RedisService, Depends(get_redis_service)],
) -> AuthService:
    return AuthService(repo=repository, redis=redis)

def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository)

# --- Current user resolution -------------------------------------------------
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    redis: Annotated[RedisService, Depends(get_redis_service)],
) -> User:
    payload = decode_token(token, expected_type=TokenType.ACCESS)

    if await redis.is_access_token_denylisted(payload["jti"]):
        raise InvalidTokenError("Token has been revoked")

    user = await repository.get_by_id(uuid.UUID(payload["sub"]))
    if user is None:
        raise InvalidTokenError("User no longer exists")
    if not user.is_active:
        raise InactiveUserError()

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]