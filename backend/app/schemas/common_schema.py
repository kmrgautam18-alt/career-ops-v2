from typing import Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Any | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: Any | None = None


class Pagination(BaseModel):
    page: int
    size: int
    total: int


class PaginatedResponse(BaseModel):
    success: bool
    message: str
    pagination: Pagination
    data: list[Any]
