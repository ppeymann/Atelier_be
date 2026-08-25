from __future__ import annotations
from typing import Any
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as starletteHTTPException

from app.core.logging import get_logger

logger = get_logger(__name__)

class AppException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "APPLICATION_ERROR"
    
    def __init__(self, message:str, *, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)
        
class NotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "NOT_FOUND"

class UserNotFoundError(NotFoundError):
    error_code = "USER_NOT_FOUND"
    
    def __init__(self) -> None:
        super().__init__("User not found")

class PageMustBiggerThan(AppException):
    error_code = "PAGE_MUST_BIGGER_THAN_ONE"
    
class PageSizeNotValid(AppException):
    error_code = "PAGE_SIZE_NOT_VALID"
        
class AlreadyExistError(AppException):
    status_code = status.HTTP_409_CONFLICT
    error_code = "ALREADY_EXISTS"
    
class InactiveUserError(AppException):
    status_code= status.HTTP_403_FORBIDDEN
    error_code="INACTIVE_USER"
    
    def __init__(self) -> None:
        super().__init__("This account has been deactivated")
    
class InvalidTokenError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "UNAUTHORIZATION"
    
class InsufficientPermissionsError(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "INSUFFICIENT_PERMISSIONS"

    def __init__(self) -> None:
        super().__init__("You do not have permission to perform this action")

    
class EmailAlreadyRegisteredError(AlreadyExistError):
    error_code = "EMAIL_ALREADY_REGISTER"
    
    def __init__(self) -> None:
        super().__init__("An account with this email already exists")
        
class PhoneAlreadyCreateClientError(AlreadyExistError):
    error_code = "PHONE_ALREADY_CREATE"
    
    def __init__(self) -> None:
        super().__init__("A client with this phone already exists")
        
class PasswordNotMatched(AppException):
    status_code= status.HTTP_422_UNPROCESSABLE_CONTENT
    error_code= "Password not matched"
    
class RateLimitExceededError(AppException):
    status_code=status.HTTP_429_TOO_MANY_REQUESTS
    error_code="RATE_LIMIT_EXCEEDED"
    
class InvalidCredentialsError(AppException):
    status_code=status.HTTP_401_UNAUTHORIZED
    error_code="INVALID_CREDENTIALS"
    
    def __init__(self) -> None:
        super().__init__("Invalid email or password")
    
    def __init__(self) -> None:
        super().__init__("Too many request. Please try again later.")

def _error_response(status_code: int, code:str, message:str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "error": {"code": code, "message":message}}
    )

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.info(
            "application_exception",
            path=request.url.path,
            error_code=exc.error_code,
            message=exc.message,
        )
        return _error_response(exc.status_code, exc.error_code, exc.message)
    @app.exception_handler(starletteHTTPException)
    async def http_exception_handler(
        request:Request,
        exc: starletteHTTPException
    ) -> JSONResponse:
        return _error_response(exc.status)
    