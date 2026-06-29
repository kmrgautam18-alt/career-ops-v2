from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.schemas.user_schema import UserLogin
from backend.app.services.auth_service import login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        email=user.email,
        password=user.password,
    )