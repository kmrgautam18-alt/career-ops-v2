from fastapi import APIRouter

from backend.app.api.v1.admin import router as admin_router
from backend.app.api.v1.ai import router as ai_router
from backend.app.api.v1.applications import router as applications_router
from backend.app.api.v1.audit_logs import router as audit_logs_router
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.auto_apply import router as auto_apply_router
from backend.app.api.v1.email_verification import router as email_verification_router
from backend.app.api.v1.export import router as export_router
from backend.app.api.v1.notification_prefs import router as notification_prefs_router
from backend.app.api.v1.oauth import router as oauth_router
from backend.app.api.v1.baserow import router as baserow_router
from backend.app.api.v1.dashboard import router as dashboard_router
from backend.app.api.v1.jobs import router as jobs_router
from backend.app.api.v1.organizations import router as organizations_router
from backend.app.api.v1.resumes import router as resumes_router
from backend.app.api.v1.users import router as users_router
from backend.app.api.v1.websocket import router as websocket_router


api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(jobs_router)
api_router.include_router(applications_router)
api_router.include_router(audit_logs_router)
api_router.include_router(admin_router)
api_router.include_router(resumes_router)
api_router.include_router(dashboard_router)
api_router.include_router(ai_router)
api_router.include_router(auto_apply_router)
api_router.include_router(oauth_router)
api_router.include_router(baserow_router)
api_router.include_router(email_verification_router)
api_router.include_router(export_router)
api_router.include_router(notification_prefs_router)
api_router.include_router(organizations_router)
api_router.include_router(websocket_router)
