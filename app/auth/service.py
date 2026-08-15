from __future__ import annotations

import uuid

from app.schemas.auth import TokenPair
from app.auth.jwt import TokenType, create_access_token, create_refresh_token, decode_token
from app.auth.password import hash_password, verify_password
from app.core.config import get_setting
from app.core.logging import get_logger
from app.models.user import User
from app.repository.user import UserRepository
from app.schemas.auth import TokenPair
from app.schemas.user import UserCreate
from app.utils.redis import RedisService as Redis
from app.core.exceptions import EmailAlreadyRegisteredError, PasswordNotMatched, RateLimitExceededError,InvalidCredentialsError

logger = get_logger(__name__)
settings = get_setting()

class AuthService:
    def __init__(self, repo: UserRepository, redis: Redis) -> None:
        self._repo = repo
        self._redis = redis
    
    async def register(self, payload: UserCreate) -> User:
        existing = await self._repo.get_by_email(payload.email)
        if existing is not None:
            raise EmailAlreadyRegisteredError()
        
        if payload.password != payload.re_password:
            raise PasswordNotMatched()
        
        user = User(
            email=payload.email,
            phone=payload.phone,
            first_name=payload.first_name,
            last_name=payload.last_name,
            hashed_password=hash_password(payload.password)
        )
        user = await self._repo.create(user)
        logger.info("user_registered", user_id=str(user.id), email=str(user.email))
        return user
    
    async def autheticate(self, email:str, password: str) -> User:
        failed_attempts = await self._redis.get_failed_login_count(email)
        if failed_attempts >= settings.LOGIN_RATE_LIMIT_PER_MINUTE:
            logger.warning("login_blocked_brute_force", email=email)
            raise RateLimitExceededError()
        
        user = await self._repo.get_by_email(email)
        if user is None or user.hashed_password is None or not verify_password(
            password, user.hashed_password
        ):
            await self._redis.register_failed_login(email)
            logger.info("login_failed", email=email)
            raise InvalidCredentialsError()
        
        await self._redis.clrear_failed_logins(email)
        logger.info("login_succeeded", user_id=str(user.id), email=email)
        return user
    
    async def issue_token_pain(self, user: User) -> TokenPair:
        access_token, expires_in = create_access_token(user_id=str(user.id))
        refresh_token, jti = create_refresh_token(user_id=str(user.id))
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in
        )
        
    