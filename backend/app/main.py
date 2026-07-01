from fastapi import FastAPI

from backend.app.api.router import api_router
from backend.app.exceptions.custom_exceptions import (
    DuplicateEmailException,
    DuplicateUsernameException,
    InactiveUserException,
    InvalidCredentialsException,
    JobNotFoundException,
    UnauthorizedException,
    UserNotFoundException,
)
from backend.app.exceptions.handlers import (
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
    ResumeNotFoundException,
    resume_not_found_exception_handler,
)

app.add_exception_handler(
    InvalidResumeFileException,
    invalid_resume_file_exception_handler,
)

app.add_exception_handler(
    UnsupportedResumeTypeException,
    unsupported_resume_type_exception_handler,
)

app.add_exception_handler(
    ResumeTooLargeException,
    resume_too_large_exception_handler,
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