from backend.app.database.base import Base
from backend.app.database.db import engine

# Import all ORM models here
from backend.app.models.job import Job
from backend.app.models.user import User
from backend.app.models.resume import Resume

def init_database():
    """
    Create all database tables defined by SQLAlchemy ORM models.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")