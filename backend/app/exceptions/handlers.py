from fastapi import Request
from fastapi.responses import JSONResponse

from backend.app.utils.logger import logger
from backend.app.exceptions.custom_exceptions import JobNotFoundException

async def job_not_found_exception_handler(
    request: Request,
    exc: JobNotFoundException
):

    logger.warning(exc.message)

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message
        }
    )

async def global_exception_handler(request: Request, exc: Exception):

    logger.exception(f"Unhandled exception: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )
