"""
Baserow Integration — REST endpoints
"""

from fastapi import APIRouter, Depends, Query

from backend.app.security.dependencies import get_current_active_user
from backend.app.services.baserow_service import BaserowService

router = APIRouter(
    prefix="/baserow",
    tags=["Baserow"],
)


def get_baserow() -> BaserowService:
    return BaserowService()


@router.get("/tables/{database_id}")
def list_tables(
    database_id: int,
    _=Depends(get_current_active_user),
    baserow: BaserowService = Depends(get_baserow),
):
    """List all tables in a Baserow database."""
    tables = baserow.list_tables(database_id)
    return {"success": True, "data": tables}


@router.get("/tables/{table_id}/rows")
def list_rows(
    table_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(100, ge=1, le=200),
    search: str = "",
    _=Depends(get_current_active_user),
    baserow: BaserowService = Depends(get_baserow),
):
    """List rows from a Baserow table with pagination."""
    result = baserow.list_rows(table_id, page=page, size=size, search=search)
    return {"success": True, "data": result}


@router.get("/tables/{table_id}/rows/{row_id}")
def get_row(
    table_id: int,
    row_id: int,
    _=Depends(get_current_active_user),
    baserow: BaserowService = Depends(get_baserow),
):
    """Get a single row by ID."""
    row = baserow.get_row(table_id, row_id)
    return {"success": True, "data": row}


@router.post("/tables/{table_id}/rows")
def create_row(
    table_id: int,
    data: dict,
    _=Depends(get_current_active_user),
    baserow: BaserowService = Depends(get_baserow),
):
    """Insert a new row. Use field_{id} keys for values."""
    row = baserow.create_row(table_id, data)
    return {"success": True, "data": row}


@router.patch("/tables/{table_id}/rows/{row_id}")
def update_row(
    table_id: int,
    row_id: int,
    data: dict,
    _=Depends(get_current_active_user),
    baserow: BaserowService = Depends(get_baserow),
):
    """Partially update a row."""
    row = baserow.update_row(table_id, row_id, data)
    return {"success": True, "data": row}


@router.delete("/tables/{table_id}/rows/{row_id}")
def delete_row(
    table_id: int,
    row_id: int,
    _=Depends(get_current_active_user),
    baserow: BaserowService = Depends(get_baserow),
):
    """Delete a row."""
    baserow.delete_row(table_id, row_id)
    return {"success": True, "message": "Row deleted successfully."}


@router.get("/health")
def health(
    _=Depends(get_current_active_user),
    baserow: BaserowService = Depends(get_baserow),
):
    """Check the Baserow connection."""
    ok = baserow.check_connection()
    return {
        "success": ok,
        "message": "Baserow connection is healthy." if ok else "Baserow connection failed.",
    }
