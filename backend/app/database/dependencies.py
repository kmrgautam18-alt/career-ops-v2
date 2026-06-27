from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Creates a database session for each request and
    automatically closes it after the request finishes.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
