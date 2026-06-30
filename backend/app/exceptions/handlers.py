from fastapi import Request
from fastapi.responses import JSONResponse

from backend.app.utils.logger import logger

from backend.app.exceptions.custom_exceptions import (
    JobNotFoundException,
    DuplicateEmailException,
    DuplicateUsernameException,
    UserNotFoundException,
    InvalidCredentialsException,
    InactiveUserException,
    UnauthorizedException,
)

from backend.app.exceptions.resume_exceptions import (
    ResumeNotFoundException,
    InvalidResumeFileException,
    UnsupportedResumeTypeException,
    ResumeTooLargeException,
)


async def job_not_found_exception_handler(
    request: Request,
    exc: JobNotFoundException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def duplicate_email_exception_handler(
    request: Request,
    exc: DuplicateEmailException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def duplicate_username_exception_handler(
    request: Request,
    exc: DuplicateUsernameException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def user_not_found_exception_handler(
    request: Request,
    exc: UserNotFoundException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def invalid_credentials_exception_handler(
    request: Request,
    exc: InvalidCredentialsException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def inactive_user_exception_handler(
    request: Request,
    exc: InactiveUserException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=403,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def unauthorized_exception_handler(
    request: Request,
    exc: UnauthorizedException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def resume_not_found_exception_handler(
    request: Request,
    exc: ResumeNotFoundException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def invalid_resume_file_exception_handler(
    request: Request,
    exc: InvalidResumeFileException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def unsupported_resume_type_exception_handler(
    request: Request,
    exc: UnsupportedResumeTypeException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=415,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def resume_too_large_exception_handler(
    request: Request,
    exc: ResumeTooLargeException,
):
    logger.warning(exc.message)

    return JSONResponse(
        status_code=413,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(f"Unhandled exception: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
        },
    )