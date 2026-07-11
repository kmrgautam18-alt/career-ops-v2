from fastapi import APIRouter

from backend.app.schemas.ats_schema import (
    ATSRequest,
    ATSResponse,
    ResumeOptimizerRequest,
    ResumeOptimizerResponse,
)
from backend.app.schemas.interview_schema import (
    InterviewQuestionResponse,
    InterviewRequest,
    InterviewResponse,
)
from backend.app.services.ai.ats.ats_service import ATSService
from backend.app.services.ai.interview.interview_service import (
    InterviewService,
)
from backend.app.services.ai.resume_optimizer.service import (
    ResumeOptimizerService,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/ats-score",
    response_model=ATSResponse,
)
def ats_score(request: ATSRequest):
    return ATSService.evaluate_resume(
        resume_text=request.resume_text,
        required_keywords=request.required_keywords,
    )


@router.post(
    "/resume-optimize",
    response_model=ResumeOptimizerResponse,
)
def resume_optimize(request: ResumeOptimizerRequest):
    return ResumeOptimizerService.optimize_resume(
        resume_text=request.resume_text,
        required_keywords=request.required_keywords,
    )


@router.post(
    "/interview/questions",
    response_model=InterviewResponse,
)
def interview_questions(request: InterviewRequest):
    report = InterviewService.generate_questions(
        skills=request.skills,
        difficulty=request.difficulty,
    )

    return InterviewResponse(
        questions=[
            InterviewQuestionResponse(
                question=q.question,
                category=q.category,
                difficulty=q.difficulty,
            )
            for q in report.questions
        ]
    )