import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application configuration loaded from environment variables.
    """

    # ======================================
    # Application
    # ======================================

    APP_NAME: str = os.getenv("APP_NAME", "Career-Ops")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # ======================================
    # Database
    # ======================================

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///data/careerops.db",
    )

    # PostgreSQL connection pool settings
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "10"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))

    # ======================================
    # CORS
    # ======================================

    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000",
    ).split(",")

    CORS_ALLOW_CREDENTIALS: bool = (
        os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    )

    # ======================================
    # Baserow (No-Code Database)
    # ======================================

    BASEROW_URL: str = os.getenv(
        "BASEROW_URL",
        "https://api.baserow.io",
    )

    BASEROW_TOKEN: str = os.getenv(
        "BASEROW_TOKEN",
        "",
    )

    # ======================================
    # JWT Security
    # ======================================

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key",
    )

    ALGORITHM: str = os.getenv(
        "ALGORITHM",
        "HS256",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # ======================================
    # LLM / AI Provider
    # ======================================

    LLM_API_KEY: str = os.getenv(
        "LLM_API_KEY",
        "",
    )

    LLM_MODEL: str = os.getenv(
        "LLM_MODEL",
        "gemini-2.0-flash",
    )

    LLM_PROVIDER: str = os.getenv(
        "LLM_PROVIDER",
        "google",
    )


settings = Settings()
