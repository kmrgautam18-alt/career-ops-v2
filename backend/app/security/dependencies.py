from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.core.roles import Roles
from backend.app.database.dependencies import get_db
from backend.app.exceptions.custom_exceptions import (
    ForbiddenException,
    InactiveUserException,
    UnauthorizedException,
)
from backend.app.repositories.user_repository_sa import (
    get_user_by_id,
)
from backend.app.security.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Return the authenticated user.
    """

    try:
        payload = decode_token(token)
    except Exception as err:
        raise UnauthorizedException() from err

    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError) as err:
        raise UnauthorizedException() from err

    user = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise UnauthorizedException()

    return user


def get_current_active_user(
    current_user=Depends(get_current_user),
):
    """
    Return only active users.
    """

    if not current_user.is_active:
        raise InactiveUserException()

    return current_user


def get_current_admin_user(
    current_user=Depends(get_current_active_user),
):
    """
    Return only admin users.
    """

    if current_user.role != Roles.ADMIN:
        raise ForbiddenException()

    return current_user