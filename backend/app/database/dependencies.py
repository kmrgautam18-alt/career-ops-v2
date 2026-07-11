from collections.abc import Generator

from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Creates a database session for each request.

    - Commit if request succeeds
    - Rollback on exception
    - Always close session
    """

    db = SessionLocal()

    try:
        yield db
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()