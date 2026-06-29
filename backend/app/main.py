from fastapi import FastAPI

from backend.app.api.router import api_router

from backend.app.exceptions.handlers import (
    global_exception_handler,
    job_not_found_exception_handler,
    duplicate_email_exception_handler,
    duplicate_username_exception_handler,
    user_not_found_exception_handler,
    invalid_credentials_exception_handler,
    inactive_user_exception_handler,
    unauthorized_exception_handler,
)

from backend.app.exceptions.custom_exceptions import (
    JobNotFoundException,
    DuplicateEmailException,
    DuplicateUsernameException,
    UserNotFoundException,
    InvalidCredentialsException,
    InactiveUserException,
    UnauthorizedException,
)

app = FastAPI(
    title="Career-Ops v2",
    version="0.1.0",
)

app.add_exception_handler(
    JobNotFoundException,
    job_not_found_exception_handler,
)

app.add_exception_handler(
    DuplicateEmailException,
    duplicate_email_exception_handler,
)

app.add_exception_handler(
    DuplicateUsernameException,
    duplicate_username_exception_handler,
)

app.add_exception_handler(
    UserNotFoundException,
    user_not_found_exception_handler,
)

app.add_exception_handler(
    InvalidCredentialsException,
    invalid_credentials_exception_handler,
)

app.add_exception_handler(
    InactiveUserException,
    inactive_user_exception_handler,
)

app.add_exception_handler(
    UnauthorizedException,
    unauthorized_exception_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)


@app.get("/")
def root():
    return {
        "application": "Career-Ops v2",
        "status": "healthy",
    }


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )