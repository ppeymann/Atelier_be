from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse

from app.api.dependencies import CurrentUser, get_auth_service
from app.auth.jwt import TokenType, decode_token
from app.core.exceptions import InvalidTokenError
from app.schemas.auth import AccessTokenResponse, LoginRequest, RefreshRequest
from app.schemas.user import UserCreate, UserRead
from app.auth.service import AuthService
from app.core.security import refresh_cookie_settings

REFRESH_COOKIE_NAME = "refresh_token"

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserRead:
    user = await auth_service.register(payload)
    return UserRead.model_validate(user)

@router.post("/login", response_model=AccessTokenResponse)
async def login(
    payload:LoginRequest,
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> AccessTokenResponse:
    user = await auth_service.autheticate(payload.email, payload.password)
    token = await auth_service.issue_token_pain(user)
    
    response.set_cookie(
        REFRESH_COOKIE_NAME,
        token.refresh_token,
        max_age=None,
        **refresh_cookie_settings(),
    )
    
    return AccessTokenResponse(access_token=token.access_token, expires_in=token.expires_in)
