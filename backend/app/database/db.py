import sqlite3

from backend.app.core.config import settings

DB_PATH = settings.DATABASE_URL.replace("sqlite:///", "")

def get_connection():
    return sqlite3.connect(DB_PATH)
