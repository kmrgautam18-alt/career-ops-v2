from sqlalchemy.orm import Session

from backend.app.repositories.user_repository_sa import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_user_by_id,
    update_user,
    delete_user,
)

from backend.app.schemas.common_schema import ApiResponse
from backend.app.schemas.user_schema import UserResponse

from backend.app.security.password import hash_password

from backend.app.exceptions.custom_exceptions import (
    DuplicateEmailException,
    DuplicateUsernameException,
    UserNotFoundException,
)


def register_user(
    db: Session,
    email: str,
    username: str,
    full_name: str,
    password: str,
):
    """
    Register a new user.
    """

    if get_user_by_email(db, email):
        raise DuplicateEmailException(email)

    if get_user_by_username(db, username):
        raise DuplicateUsernameException(username)

    user = create_user(
        db=db,
        email=email,
        username=username,
        full_name=full_name,
        hashed_password=hash_password(password),
    )

    return ApiResponse(
        success=True,
        message="User registered successfully.",
        data=UserResponse.model_validate(user),
    )


def get_user(
    db: Session,
    user_id: int,
):
    """
    Retrieve user by ID.
    """

    user = get_user_by_id(db, user_id)

    if user is None:
        raise UserNotFoundException(user_id)

    return ApiResponse(
        success=True,
        message="User retrieved successfully.",
        data=UserResponse.model_validate(user),
    )


def get_current_user_profile(
    current_user,
):
    """
    Return authenticated user profile.
    """

    return ApiResponse(
        success=True,
        message="Current user retrieved successfully.",
        data=UserResponse.model_validate(current_user),
    )


def update_existing_user(
    db: Session,
    user,
):
    """
    Update an existing user.
    """

    updated_user = update_user(
        db=db,
        user=user,
    )

    return ApiResponse(
        success=True,
        message="User updated successfully.",
        data=UserResponse.model_validate(updated_user),
    )


def delete_existing_user(
    db: Session,
    user,
):
    """
    Delete an existing user.
    """

    delete_user(
        db=db,
        user=user,
    )

    return ApiResponse(
        success=True,
        message="User deleted successfully.",
        data=None,
    )