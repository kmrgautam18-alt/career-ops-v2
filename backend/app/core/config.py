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

    # ======================================
    # n8n Webhook (Workflow Automation)
    # ======================================

    N8N_WEBHOOK_BASE_URL: str = os.getenv(
        "N8N_WEBHOOK_BASE_URL",
        "http://n8n:5678",
    )

    N8N_ENABLED: bool = os.getenv("N8N_ENABLED", "false").lower() == "true"

    # ======================================
    # SMTP / Email
    # ======================================

    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "careerops@example.com")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME", "Career-Ops Auto-Apply")
    SMTP_TLS: bool = os.getenv("SMTP_TLS", "true").lower() == "true"
    SMTP_ENABLED: bool = os.getenv("SMTP_ENABLED", "false").lower() == "true"

    # ======================================
    # Auto-Apply Engine
    # ======================================

    AUTO_APPLY_DAILY_LIMIT: int = int(os.getenv("AUTO_APPLY_DAILY_LIMIT", "20"))
    AUTO_APPLY_INTERVIEW_FOLLOWUP_DAYS: int = int(
        os.getenv("AUTO_APPLY_INTERVIEW_FOLLOWUP_DAYS", "3")
    )

    # ======================================
    # Redis Cache
    # ======================================

    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "true").lower() == "true"
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    # ======================================
    # Celery (Background Tasks)
    # ======================================

    CELERY_ENABLED: bool = os.getenv("CELERY_ENABLED", "false").lower() == "true"
    CELERY_BROKER_URL: str = os.getenv(
        "CELERY_BROKER_URL",
        "redis://redis:6379/1",
    )
    CELERY_RESULT_BACKEND: str = os.getenv(
        "CELERY_RESULT_BACKEND",
        "redis://redis:6379/2",
    )

    # ======================================
    # OAuth (Social Login)
    # ======================================

    OAUTH_ENABLED: bool = os.getenv("OAUTH_ENABLED", "true").lower() == "true"

    # Google OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")

    # GitHub OAuth
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID", "")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET", "")


settings = Settings()
