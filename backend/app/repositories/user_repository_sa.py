from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.user import User


def create_user(
    db: Session,
    email: str,
    username: str,
    full_name: str,
    hashed_password: str,
):
    """
    Create a new user.
    """

    user = User(
        email=email,
        username=username,
        full_name=full_name,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(
    db: Session,
    user_id: int,
):
    """
    Retrieve user by ID.
    """

    return db.get(User, user_id)


def get_user_by_email(
    db: Session,
    email: str,
):
    """
    Retrieve user by email.
    """

    return db.scalar(
        select(User).where(User.email == email)
    )


def get_user_by_username(
    db: Session,
    username: str,
):
    """
    Retrieve user by username.
    """

    return db.scalar(
        select(User).where(User.username == username)
    )


def update_user(
    db: Session,
    user: User,
):
    """
    Persist user updates.
    """

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User,
):
    """
    Delete a user.
    """

    db.delete(user)
    db.commit()

    return True