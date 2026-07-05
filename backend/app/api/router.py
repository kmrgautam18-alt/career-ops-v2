from fastapi import APIRouter

from backend.app.api.v1.admin import router as admin_router
from backend.app.api.v1.applications import router as applications_router
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.dashboard import router as dashboard_router
from backend.app.api.v1.jobs import router as jobs_router
from backend.app.api.v1.resumes import router as resumes_router
from backend.app.api.v1.users import router as users_router

api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(jobs_router)
api_router.include_router(applications_router)
api_router.include_router(admin_router)
api_router.include_router(resumes_router)

api_router.include_router(dashboard_router)
