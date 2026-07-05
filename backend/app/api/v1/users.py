from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.schemas.user_schema import UserCreate
from backend.app.security.dependencies import (
    get_current_active_user,
)
from backend.app.services.user_service import (
    get_current_user_profile,
    get_user,
    register_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/register")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    return register_user(
        db=db,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        password=user.password,
    )


@router.get("/me")
def get_my_profile(
    current_user=Depends(get_current_active_user),
):
    """
    Return currently authenticated user's profile.
    """

    return get_current_user_profile(
        current_user=current_user,
    )


@router.get("/{user_id}")
def get_single_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Get user by ID.
    """

    return get_user(
        db=db,
        user_id=user_id,
    )
