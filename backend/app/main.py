from typing import cast

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ExceptionHandler

from backend.app.api.router import api_router
from backend.app.core.config import settings
from backend.app.services.health import health_router
from backend.app.services.metrics import get_metrics
from backend.app.services.rate_limiter import add_rate_limiting
from backend.app.core.config import settings
from backend.app.exceptions.custom_exceptions import (
    ApplicationNotFoundException,
    DuplicateEmailException,
    DuplicateUsernameException,
    InactiveUserException,
    InvalidCredentialsException,
    JobNotFoundException,
    UnauthorizedException,
    UserNotFoundException,
)

# ======================================
# Sentry Error Tracking (if configured)
# ======================================
try:
    if settings.APP_ENV == "production" and os.getenv("SENTRY_DSN"):
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=os.getenv("SENTRY_DSN"),
            environment=settings.APP_ENV,
            traces_sample_rate=0.2,
            profiles_sample_rate=0.1,
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
            ],
        )
        print("Sentry initialized.")
except ImportError:
    pass
except Exception as e:
    print(f"Sentry init failed: {e}")
from backend.app.exceptions.handlers import (
    application_not_found_exception_handler,
    duplicate_email_exception_handler,
    duplicate_username_exception_handler,
    global_exception_handler,
    inactive_user_exception_handler,
    invalid_credentials_exception_handler,
    invalid_resume_file_exception_handler,
    job_not_found_exception_handler,
    resume_not_found_exception_handler,
    resume_too_large_exception_handler,
    unauthorized_exception_handler,
    unsupported_resume_type_exception_handler,
    user_not_found_exception_handler,
)
from backend.app.exceptions.resume_exceptions import (
    InvalidResumeFileException,
    ResumeNotFoundException,
    ResumeTooLargeException,
    UnsupportedResumeTypeException,
)

app = FastAPI(
    title="Career-Ops v2",
    version="0.2.0",
)

# ======================================
# CORS Middleware (Production)
# ======================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    JobNotFoundException,
    cast(ExceptionHandler, job_not_found_exception_handler),
)

app.add_exception_handler(
    ApplicationNotFoundException,
    cast(ExceptionHandler, application_not_found_exception_handler),
)

app.add_exception_handler(
    DuplicateEmailException,
    cast(ExceptionHandler, duplicate_email_exception_handler),
)

app.add_exception_handler(
    DuplicateUsernameException,
    cast(ExceptionHandler, duplicate_username_exception_handler),
)

app.add_exception_handler(
    UserNotFoundException,
    cast(ExceptionHandler, user_not_found_exception_handler),
)

app.add_exception_handler(
    InvalidCredentialsException,
    cast(ExceptionHandler, invalid_credentials_exception_handler),
)

app.add_exception_handler(
    InactiveUserException,
    cast(ExceptionHandler, inactive_user_exception_handler),
)

app.add_exception_handler(
    UnauthorizedException,
    cast(ExceptionHandler, unauthorized_exception_handler),
)

app.add_exception_handler(
    ResumeNotFoundException,
    cast(ExceptionHandler, resume_not_found_exception_handler),
)

app.add_exception_handler(
    InvalidResumeFileException,
    cast(ExceptionHandler, invalid_resume_file_exception_handler),
)

app.add_exception_handler(
    UnsupportedResumeTypeException,
    cast(ExceptionHandler, unsupported_resume_type_exception_handler),
)

app.add_exception_handler(
    ResumeTooLargeException,
    cast(ExceptionHandler, resume_too_large_exception_handler),
)

app.add_exception_handler(
    Exception,
    cast(ExceptionHandler, global_exception_handler),
)


@app.get("/")
def root():

    return {
        "application": "Career-Ops v2",
        "status": "healthy",
    }


# ======================================
# Prometheus Metrics Endpoint
# ======================================


@app.get("/metrics")
def metrics():
    """
    Expose Prometheus metrics for scraping.
    """
    from starlette.responses import Response

    return Response(
        content=get_metrics(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )


# ======================================
# Rate Limiting (Production)
# ======================================

add_rate_limiting(app)

# ======================================
# Health Check Endpoints
# ======================================

app.include_router(health_router)


app.include_router(api_router)


# ======================================
# WebSocket endpoint (mounted at /api/v1/ws)
# ======================================
from backend.app.api.v1.websocket import router as websocket_router
app.include_router(websocket_router)

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
