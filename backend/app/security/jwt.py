# ruff: noqa: UP017
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from jose import JWTError, jwt

from backend.app.core.config import settings


def create_access_token(
    user_id: int,
    email: str,
    role: str,
) -> str:
    """
    Generate JWT access token.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "type": "access",
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "jti": str(uuid4()),
    }

    return str(
        jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
    )


def create_refresh_token(
    user_id: int,
) -> str:
    """
    Generate JWT refresh token.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "jti": str(uuid4()),
    }

    return str(
        jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
    )


def decode_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode JWT token.
    """

    return dict(
        jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    )


def verify_token(
    token: str,
) -> bool:
    """
    Verify JWT token.
    """

    try:
        decode_token(token)
        return True

    except JWTError:
        return False
