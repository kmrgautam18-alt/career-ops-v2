from fastapi import APIRouter

from backend.app.api.v1.jobs import router as jobs_router
from backend.app.api.v1.users import router as users_router

api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(jobs_router)
api_router.include_router(users_router)