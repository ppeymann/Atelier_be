from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class ErrorDetail(BaseModel):
    code: str
    message: str
    
class ErrorResponse(BaseModel):
    success: bool
    error: str

class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    meta: dict[str, str | int | float | bool] | None = None
    
class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_page: int
    
class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T]
    meta: PaginationMeta