from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.schemas.user_schema import (
    RefreshTokenRequest,
    UserLogin,
)
from backend.app.security.dependencies import (
    get_current_active_user,
)
from backend.app.services.auth_service import (
    login_user,
    logout_user,
    refresh_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate user.
    """

    return login_user(
        db=db,
        email=user.email,
        password=user.password,
    )


@router.post("/refresh")
def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Refresh access token.
    """

    return refresh_access_token(
        db=db,
        refresh_token=request.refresh_token,
    )


@router.post("/logout")
def logout(
    current_user=Depends(get_current_active_user),
):
    """
    Logout authenticated user.
    """

    return logout_user()