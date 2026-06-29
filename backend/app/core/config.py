from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    # ======================================
    # Application
    # ======================================
    APP_NAME = os.getenv("APP_NAME")
    APP_VERSION = os.getenv("APP_VERSION")
    APP_ENV = os.getenv("APP_ENV")
    DEBUG = os.getenv("DEBUG")

    # ======================================
    # Database
    # ======================================
    DATABASE_URL = os.getenv("DATABASE_URL")

    # ======================================
    # JWT Security
    # ======================================
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    REFRESH_TOKEN_EXPIRE_DAYS = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
    )


settings = Settings()