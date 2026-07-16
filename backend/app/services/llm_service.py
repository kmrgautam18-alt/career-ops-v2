"""
LLM service for Career-Ops AI features.
Wraps Google Gemini with structured prompt engineering
for ATS scoring, interview questions, resume optimization, and job matching.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """Raised when the LLM service fails."""


def _get_model() -> Any | None:
    """Initialize and return the Gemini model, or None if unavailable."""
    if not settings.LLM_API_KEY:
        logger.warning("LLM_API_KEY is not set. AI features will use fallback logic.")
        return None

    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.LLM_API_KEY)
        model = genai.GenerativeModel(
            settings.LLM_MODEL,
            generation_config={
                "temperature": 0.3,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            },
        )
        return model
    except Exception as e:
        logger.error(f"Failed to initialize Gemini model: {e}")
        return None


_model_instance: Any | None = None


def get_model() -> Any | None:
    """Lazy-loaded singleton for the Gemini model instance."""
    global _model_instance
    if _model_instance is None:
        _model_instance = _get_model()
    return _model_instance


def _call_llm(prompt: str, system_instruction: str = "") -> str:
    """Call the Gemini model with a prompt and return the text response."""
    model = get_model()
    if model is None:
        raise LLMServiceError("LLM is not configured. Set LLM_API_KEY in environment.")

    try:
        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [system_instruction]})
        contents.append({"role": "user", "parts": [prompt]})

        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise LLMServiceError(f"LLM call failed: {e}") from e


def _call_llm_json(prompt: str, system_instruction: str = "") -> dict[str, Any]:
    """Call the LLM and parse the response as JSON."""
    text = _call_llm(prompt, system_instruction)
    # Strip markdown code fences if present
    text = text.strip()
    if text.startswith("```"):
        # Extract content between ```json and ```
        lines = text.split("\n")
        start = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("```"):
                start = i + 1
                break
        end = len(lines)
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith("```"):
                end = i
                break
        text = "\n".join(lines[start:end]).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.warning(f"LLM response was not valid JSON: {e}")
        logger.debug(f"Raw response: {text}")
        raise LLMServiceError(f"Failed to parse LLM response as JSON: {e}") from e


# =============================================================================
# Prompt Templates
# =============================================================================

ATS_SYSTEM_PROMPT = """You are an expert ATS (Applicant Tracking System) evaluator and career coach.
Analyze resumes against job descriptions with precision.
Return ONLY valid JSON without markdown formatting."""

ATS_SCORE_PROMPT = """Analyze this resume against the job description and return a JSON object with:
- overall_score (0-100): Overall match percentage
- keyword_score (0-100): How well keywords from job description appear in resume
- formatting_score (0-100): Resume structure and clarity
- section_score (0-100): Presence of required sections (summary, experience, education, skills)
- readability_score (0-100): Clarity and readability
- strengths (array of strings): Key strengths of the resume for this job
- weaknesses (array of strings): Areas needing improvement
- recommendations (array of objects with 'title', 'description', 'priority'): Actionable recommendations

Resume:
---
{resume_text}
---

Job Description:
---
{job_description}
---
"""

INTERVIEW_SYSTEM_PROMPT = """You are an expert technical interviewer and career coach.
Generate realistic, high-quality interview questions for specific roles and companies.
Return ONLY valid JSON without markdown formatting."""

INTERVIEW_QUESTIONS_PROMPT = """Generate {count} interview questions for a {job_title} position at {company}.

Difficulty level: {difficulty}

Return a JSON object with:
- questions (array of objects with 'question', 'category', 'difficulty')

Cover these categories: technical skills, behavioral, system design, problem-solving.
Vary the difficulty across easy, medium, and hard levels as appropriate.
"""

RESUME_OPTIMIZE_SYSTEM_PROMPT = """You are an expert resume optimization consultant.
Analyze resumes against job descriptions and suggest concrete improvements.
Return ONLY valid JSON without markdown formatting."""

RESUME_OPTIMIZE_PROMPT = """Analyze this resume against the job description and return a JSON object with:
- ats_score_before (0-100): Estimated current ATS score
- ats_score_after (0-100): Estimated score after applying suggestions
- missing_keywords (array of strings): Important keywords missing from the resume
- suggestions (array of objects with 'title', 'current', 'suggested', 'priority'): Specific improvements

Resume:
---
{resume_text}
---

Job Description:
---
{job_description}
---
"""


# =============================================================================
# Public API
# =============================================================================

def ats_evaluate(resume_text: str, job_description: str) -> dict[str, Any]:
    """Evaluate a resume against a job description using AI."""
    prompt = ATS_SCORE_PROMPT.format(
        resume_text=resume_text[:8000],
        job_description=job_description[:8000],
    )
    return _call_llm_json(prompt, ATS_SYSTEM_PROMPT)


def generate_interview_questions(
    job_title: str,
    company: str,
    difficulty: str = "medium",
    count: int = 8,
) -> list[dict[str, str]]:
    """Generate interview questions for a specific role using AI."""
    prompt = INTERVIEW_QUESTIONS_PROMPT.format(
        job_title=job_title,
        company=company,
        difficulty=difficulty,
        count=count,
    )
    result = _call_llm_json(prompt, INTERVIEW_SYSTEM_PROMPT)
    return result.get("questions", [])


def optimize_resume(resume_text: str, job_description: str) -> dict[str, Any]:
    """Analyze and suggest resume optimizations using AI."""
    prompt = RESUME_OPTIMIZE_PROMPT.format(
        resume_text=resume_text[:8000],
        job_description=job_description[:8000],
    )
    return _call_llm_json(prompt, RESUME_OPTIMIZE_SYSTEM_PROMPT)
