from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError as PyJWTInvalidTokenError

from app.core.exceptions import InvalidTokenError
from app.core.config import get_setting

settings = get_setting()

class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
    
def _create_token(
    *, subject: str, token_type: TokenType, expires_delta: timedelta
) -> tuple[str, str]:
    now = datetime.now(UTC)
    jti = str(uuid.uuid4())
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "jti":jti,
        "iat":now,
        "exp": now + expires_delta
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token, jti

def create_access_token(*, user_id: str) -> tuple[str, int]:
    expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token, _jti = _create_token(
        subject=user_id, token_type=TokenType.ACCESS, expires_delta=expires_delta
    )
    return token, int(expires_delta.total_seconds())

def create_refresh_token(*, user_id: str) -> tuple[str, str]:
    expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(
        subject=user_id, token_type=TokenType.REFRESH, expires_delta=expires_delta
    ) 
    
def decode_token(token: str, *, expected_type: TokenType) -> dict[str, Any]:
    try:
        payload=jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except ExpiredSignatureError as exc:
        raise InvalidTokenError("Token has expired") from exc
    except PyJWTInvalidTokenError:
        raise InvalidTokenError("Token is invalid") from exc
    
    if payload.get("type") != expected_type.value:
        raise InvalidTokenError(f"Expected a {expected_type.value} token")
    
    return payload
    
    
