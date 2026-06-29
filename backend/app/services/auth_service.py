from sqlalchemy.orm import Session

from backend.app.repositories.user_repository_sa import get_user_by_email

from backend.app.security.password import verify_password
from backend.app.security.jwt import (
    create_access_token,
    create_refresh_token,
)

from backend.app.schemas.common_schema import ApiResponse

from backend.app.exceptions.custom_exceptions import (
    InvalidCredentialsException,
    InactiveUserException,
)


def login_user(
    db: Session,
    email: str,
    password: str,
):
    """
    Authenticate user and generate JWT tokens.
    """

    user = get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        raise InvalidCredentialsException()

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise InvalidCredentialsException()

    if not user.is_active:
        raise InactiveUserException()

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role,
    )

    refresh_token = create_refresh_token(
        user_id=user.id,
    )

    return ApiResponse(
        success=True,
        message="Login successful.",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
    )