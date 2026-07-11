from fastapi import APIRouter

from backend.app.schemas.ats_schema import (
    ATSRequest,
    ResumeOptimizerRequest,
)
from backend.app.services.ai.ats.ats_service import (
    ATSService,
)
from backend.app.services.ai.resume_optimizer.service import (
    ResumeOptimizerService,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/ats-score")
def ats_score(
    request: ATSRequest,
):
    """
    Evaluate ATS score for a resume.
    """

    return ATSService.evaluate_resume(
        resume_text=request.resume_text,
        required_keywords=request.required_keywords,
    )


@router.post("/resume-optimize")
def resume_optimize(
    request: ResumeOptimizerRequest,
):
    """
    Optimize resume for ATS.
    """

    return ResumeOptimizerService.optimize_resume(
        resume_text=request.resume_text,
        required_keywords=request.required_keywords,
    )