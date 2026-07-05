from backend.app.database.base import Base
from backend.app.database.db import engine

# Import ORM models so SQLAlchemy registers them.
from backend.app.models.application import Application  # noqa: F401
from backend.app.models.job import Job  # noqa: F401
from backend.app.models.resume import Resume  # noqa: F401
from backend.app.models.user import User  # noqa: F401


def init_database():
    """
    Create all database tables defined by SQLAlchemy ORM models.
    """

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")
