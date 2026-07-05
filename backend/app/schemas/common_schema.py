from typing import Any

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    size: int
    total: int
    pages: int


class ApiResponse(BaseModel):
    success: bool
    message: str
    pagination: Pagination | None = None
    data: Any | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: Any | None = None
