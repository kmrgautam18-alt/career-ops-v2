import sqlite3

DB_PATH = "/root/career-ops-v2/data/careerops.db"

def get_connection():
    return sqlite3.connect(DB_PATH)
