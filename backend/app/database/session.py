from sqlalchemy.orm import sessionmaker

from backend.app.database.db import engine

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
