import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

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
from backend.app.schemas.job_match_schema import (
    JobMatchRequest,
    JobMatchResponse,
)
from backend.app.services.ai.ats.ats_service import ATSService
from backend.app.services.ai.interview.interview_service import (
    InterviewService,
)
from backend.app.services.ai.resume_optimizer.service import (
    ResumeOptimizerService,
)
from backend.app.services.llm_service import (
    job_match_ai,
    stream_ats_evaluate,
    stream_interview_questions,
    stream_optimize_resume,
    stream_job_match,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


# =============================================================================
# Non-streaming endpoints
# =============================================================================

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


@router.post(
    "/job-match",
    response_model=JobMatchResponse,
)
def job_match_endpoint(request: JobMatchRequest):
    """AI-powered job match analysis between a candidate profile and job."""
    result = job_match_ai(
        profile=request.profile,
        job_details=request.job_details,
    )

    return JobMatchResponse(
        overall_score=result.get("overall_score", 50),
        classification=result.get("classification", "moderate"),
        skill=result.get("skill", {}),
        experience=result.get("experience", {}),
        education=result.get("education", {}),
        strengths=result.get("strengths", []),
        weaknesses=result.get("weaknesses", []),
        recommendations=result.get("recommendations", []),
    )


# =============================================================================
# Streaming (SSE) endpoints
# =============================================================================

async def _sse_stream(stream_gen):
    """Wrap an async generator into a StreamingResponse."""
    return StreamingResponse(stream_gen, media_type="text/event-stream")


@router.post("/ats-score/stream")
async def ats_score_stream(request: ATSRequest):
    """Stream ATS evaluation results token by token."""
    gen = stream_ats_evaluate(
        resume_text=request.resume_text,
        job_description=request.job_description,
    )
    return await _sse_stream(gen)


@router.post("/interview/questions/stream")
async def interview_questions_stream(request: InterviewRequest):
    """Stream interview question generation token by token."""
    gen = stream_interview_questions(
        job_title=request.job_title or "Professional",
        company=request.company or "Company",
        difficulty=request.difficulty,
    )
    return await _sse_stream(gen)


@router.post("/resume-optimize/stream")
async def resume_optimize_stream(request: ResumeOptimizerRequest):
    """Stream resume optimization tokens token by token."""
    gen = stream_optimize_resume(
        resume_text=request.resume_text,
        job_description=request.job_description,
    )
    return await _sse_stream(gen)


@router.post("/job-match/stream")
async def job_match_stream(request: JobMatchRequest):
    """Stream job match analysis tokens token by token."""
    gen = stream_job_match(
        profile=request.profile,
        job_details=request.job_details,
    )
    return await _sse_stream(gen)
