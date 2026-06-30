from fastapi import APIRouter, Depends

from backend.app.security.dependencies import (
    get_current_admin_user,
)

from backend.app.schemas.common_schema import ApiResponse

router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
)


@router.get("/health")
def admin_health(
    current_user=Depends(get_current_admin_user),
):
    """
    Admin-only health endpoint.
    """

    return ApiResponse(
        success=True,
        message="Admin authorization successful.",
        data={
            "status": "healthy",
            "current_user": current_user.username,
            "role": current_user.role,
        },
    )