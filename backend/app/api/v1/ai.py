from fastapi import APIRouter

from backend.app.schemas.ats_schema import (
    ATSRequest,
    ATSResponse,
    ATSScoreResponse,
    ATSRecommendationResponse,
    ResumeOptimizerRequest,
    ResumeOptimizerResponse,
    OptimizationSuggestionResponse,
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
    report = ATSService.evaluate_resume(
        resume_text=request.resume_text,
        required_keywords=request.required_keywords,
        job_description=request.job_description,
    )

    return ATSResponse(
        score=ATSScoreResponse(
            keywords=report.score.keywords,
            formatting=report.score.formatting,
            sections=report.score.sections,
            readability=report.score.readability,
            overall=report.score.overall,
        ),
        recommendations=[
            ATSRecommendationResponse(
                title=r.title,
                description=r.description,
                priority=r.priority,
            )
            for r in report.recommendations
        ],
        strengths=report.strengths,
        weaknesses=report.weaknesses,
    )


@router.post(
    "/resume-optimize",
    response_model=ResumeOptimizerResponse,
)
def resume_optimize(request: ResumeOptimizerRequest):
    report = ResumeOptimizerService.optimize_resume(
        resume_text=request.resume_text,
        required_keywords=request.required_keywords,
        job_description=request.job_description,
    )

    return ResumeOptimizerResponse(
        ats_score_before=report.ats_score_before,
        ats_score_after=report.ats_score_after,
        missing_keywords=report.missing_keywords,
        suggestions=[
            OptimizationSuggestionResponse(
                title=s.title,
                current=s.current,
                suggested=s.suggested,
                priority=s.priority,
            )
            for s in report.suggestions
        ],
    )


@router.post(
    "/interview/questions",
    response_model=InterviewResponse,
)
def interview_questions(request: InterviewRequest):
    # Use job_title and company if provided, otherwise fall back to skills
    if request.job_title and request.company:
        report = InterviewService.generate_questions(
            job_title=request.job_title,
            company=request.company,
            difficulty=request.difficulty,
        )
    else:
        report = InterviewService.generate_questions_from_skills(
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
