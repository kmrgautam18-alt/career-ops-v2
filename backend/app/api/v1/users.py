from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db

from backend.app.schemas.user_schema import UserCreate

from backend.app.services.user_service import (
    register_user,
    get_user,
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
    return register_user(
        db=db,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=user.password,  # Temporary (will hash next)
    )


@router.get("/{user_id}")
def get_single_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_user(
        db=db,
        user_id=user_id,
    )