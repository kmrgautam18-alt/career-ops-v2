from backend.app.database.base import Base
from backend.app.database.db import engine

from backend.app.models.application import Application
from backend.app.models.job import Job
from backend.app.models.resume import Resume
from backend.app.models.user import User

# Import all ORM models here


def init_database():
    """
    Create all database tables defined by SQLAlchemy ORM models.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")