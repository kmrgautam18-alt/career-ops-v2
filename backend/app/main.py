from fastapi import FastAPI

from backend.app.api.router import api_router

from backend.app.exceptions.handlers import (
    global_exception_handler,
    job_not_found_exception_handler,
)

from backend.app.exceptions.custom_exceptions import (
    JobNotFoundException,
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