from sqlalchemy.orm import Session

from backend.app.exceptions.custom_exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
    UnauthorizedException,
)
from backend.app.repositories.user_repository_sa import (
    get_user_by_email,
    get_user_by_id,
)
from backend.app.schemas.common_schema import ApiResponse
from backend.app.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from backend.app.security.password import verify_password


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


def refresh_access_token(
    db: Session,
    refresh_token: str,
):
    """
    Generate a new access token using a valid refresh token.
    """

    try:
        payload = decode_token(refresh_token)
    except Exception as err:
        raise UnauthorizedException() from err

    if payload.get("type") != "refresh":
        raise UnauthorizedException()

    user = get_user_by_id(
        db=db,
        user_id=int(payload["sub"]),
    )

    if user is None:
        raise UnauthorizedException()

    if not user.is_active:
        raise InactiveUserException()

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role,
    )

    return ApiResponse(
        success=True,
        message="Access token refreshed successfully.",
        data={
            "access_token": access_token,
            "token_type": "bearer",
        },
    )


def logout_user():
    """
    Logout the authenticated user.

    JWT is stateless.
    Client should remove access and refresh tokens.

    Future:
    Redis token blacklist will be implemented.
    """

    return ApiResponse(
        success=True,
        message="Logout successful.",
        data=None,
    )
