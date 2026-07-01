from backend.app.database.base import Base
from backend.app.database.db import engine

# Import all ORM models here


def init_database():
    """
    Create all database tables defined by SQLAlchemy ORM models.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")