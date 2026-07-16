"""
Resume Builder Service for Auto Job Application Engine.
Uses Gemini LLM to tailor resumes to specific job descriptions,
generating optimized resume text based on a user's template.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


RESUME_TAILOR_SYSTEM_PROMPT = """You are an expert resume writer and ATS optimization specialist.
Your task is to tailor a candidate's resume to match a specific job description.
Analyze the job requirements carefully and rewrite the resume to maximize keyword match
while maintaining truthfulness and professional quality.
Return ONLY valid JSON without markdown formatting."""

RESUME_TAILOR_PROMPT = """You are tailoring a resume for a specific job application.

## Candidate's Base Resume (JSON template)
{template_json}

## Job Description
{job_description}

## Company
{company}

## Job Title
{job_title}

## Instructions
1. Analyze the job description and identify key skills, qualifications, and keywords.
2. Rewrite the work experience bullet points to emphasize relevant achievements.
3. Reorder skills to put the most relevant ones first.
4. Add a professional summary tailored to this specific role (3-4 sentences).
5. Keep all information truthful — never fabricate experience.
6. Maximize ATS keyword matching without keyword stuffing.

Return a JSON object with:
- professional_summary (string): 3-4 sentence summary tailored to the role
- work_experience (string): Rewritten work experience section with bullet points
- skills (string): Reordered skills, most relevant first
- education (string): Education section (keep as-is or slightly adjust)
- certifications (string): Certifications section
- projects (string): Projects section
- ats_score_estimate (0-100): How well this tailored resume matches the job
- missing_keywords (array of strings): Important keywords from job that couldn't be matched
"""


def _call_llm_json(prompt: str, system_instruction: str = "") -> dict[str, Any]:
    """Call Gemini and parse JSON response."""
    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.LLM_API_KEY)
        model = genai.GenerativeModel(
            settings.LLM_MODEL,
            generation_config={
                "temperature": 0.3,
                "top_p": 0.95,
                "max_output_tokens": 4096,
            },
        )
        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [system_instruction]})
        contents.append({"role": "user", "parts": [prompt]})

        response = model.generate_content(contents)
        text = response.text

        # Strip markdown code fences
        text = text.strip()
        if text.startswith("```"):
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

        return json.loads(text)
    except ImportError:
        logger.warning("google.generativeai not installed")
        return _fallback_tailored_resume_parts()
    except Exception as e:
        logger.error(f"Resume builder LLM call failed: {e}")
        return _fallback_tailored_resume_parts()


def _fallback_tailored_resume_parts() -> dict[str, Any]:
    """Fallback when LLM is unavailable — returns a basic template."""
    return {
        "professional_summary": "Experienced professional with a track record of delivering results in cross-functional teams. "
        "Skilled in project management, technical execution, and stakeholder communication.",
        "work_experience": "• Led key initiatives that improved team productivity and delivered measurable outcomes\n"
        "• Collaborated with cross-functional teams to design and implement solutions\n"
        "• Managed end-to-end project lifecycle from requirements to deployment\n"
        "• Contributed to code quality and best practices through code reviews and documentation",
        "skills": "Project Management, Team Collaboration, Problem Solving, Communication, Technical Documentation",
        "education": "Bachelor's degree in relevant field",
        "certifications": "",
        "projects": "",
        "ats_score_estimate": 65,
        "missing_keywords": [],
    }


def tailor_resume(
    template_json: str,
    job_title: str,
    company: str,
    job_description: str,
) -> dict[str, Any]:
    """
    Tailor a resume to a specific job using AI.

    Args:
        template_json: JSON string of the user's base resume template
        job_title: The job title to apply for
        company: The company name
        job_description: The full job description text

    Returns:
        Dict with professional_summary, work_experience, skills, education,
        certifications, projects, ats_score_estimate, missing_keywords
    """
    if not settings.LLM_API_KEY:
        logger.info("LLM_API_KEY not set — using fallback resume tailoring")
        return _fallback_tailored_resume_parts()

    prompt = RESUME_TAILOR_PROMPT.format(
        template_json=template_json[:12000],
        job_description=job_description[:8000],
        company=company,
        job_title=job_title,
    )
    return _call_llm_json(prompt, RESUME_TAILOR_SYSTEM_PROMPT)


def build_full_resume_text(
    tailored_parts: dict[str, Any],
    full_name: str,
    email: str,
    phone: str = "",
    linkedin: str = "",
) -> str:
    """
    Assemble a formatted plain-text resume from tailored parts.

    Args:
        tailored_parts: Output from tailor_resume()
        full_name: Candidate's full name
        email: Candidate's email
        phone: Candidate's phone (optional)
        linkedin: LinkedIn URL (optional)

    Returns:
        Formatted plain-text resume ready to include in email body
    """
    lines = []
    header = full_name.upper()
    lines.append("=" * 60)
    lines.append(f"{header:^60}")
    lines.append("=" * 60)

    contact = email
    if phone:
        contact += f" | {phone}"
    if linkedin:
        contact += f" | {linkedin}"
    lines.append(contact)
    lines.append("")

    # Professional Summary
    summary = tailored_parts.get("professional_summary", "")
    if summary:
        lines.append("─" * 60)
        lines.append("PROFESSIONAL SUMMARY")
        lines.append("─" * 60)
        lines.append(summary)
        lines.append("")

    # Skills
    skills = tailored_parts.get("skills", "")
    if skills:
        lines.append("─" * 60)
        lines.append("SKILLS")
        lines.append("─" * 60)
        lines.append(skills)
        lines.append("")

    # Work Experience
    experience = tailored_parts.get("work_experience", "")
    if experience:
        lines.append("─" * 60)
        lines.append("WORK EXPERIENCE")
        lines.append("─" * 60)
        lines.append(experience)
        lines.append("")

    # Education
    education = tailored_parts.get("education", "")
    if education:
        lines.append("─" * 60)
        lines.append("EDUCATION")
        lines.append("─" * 60)
        lines.append(education)
        lines.append("")

    # Certifications
    certs = tailored_parts.get("certifications", "")
    if certs:
        lines.append("─" * 60)
        lines.append("CERTIFICATIONS")
        lines.append("─" * 60)
        lines.append(certs)
        lines.append("")

    # Projects
    projects = tailored_parts.get("projects", "")
    if projects:
        lines.append("─" * 60)
        lines.append("PROJECTS")
        lines.append("─" * 60)
        lines.append(projects)

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


def generate_cover_letter(
    full_name: str,
    job_title: str,
    company: str,
    job_description: str,
    template_json: str = "",
) -> str:
    """
    Generate a tailored cover letter for a specific job.

    Args:
        full_name: Applicant's name
        job_title: Job title
        company: Company name
        job_description: Job description text
        template_json: Optional resume template for context

    Returns:
        Cover letter text
    """
    if not settings.LLM_API_KEY:
        return _fallback_cover_letter(full_name, job_title, company)

    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.LLM_API_KEY)
        model = genai.GenerativeModel(
            settings.LLM_MODEL,
            generation_config={"temperature": 0.4, "max_output_tokens": 1024},
        )

        prompt = (
            f"Write a professional cover letter for {full_name} applying for "
            f"the {job_title} position at {company}.\n\n"
            f"Job Description:\n{job_description[:4000]}\n\n"
            f"Resume Context:\n{template_json[:3000] if template_json else 'N/A'}\n\n"
            "Keep it to 3-4 paragraphs. Be specific, enthusiastic, and professional. "
            "Do not include placeholders like [Your Name] — use the name provided."
        )

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.warning(f"Cover letter generation failed: {e}")
        return _fallback_cover_letter(full_name, job_title, company)


def _fallback_cover_letter(full_name: str, job_title: str, company: str) -> str:
    """Fallback cover letter when AI is unavailable."""
    return (
        f"Dear Hiring Team,\n\n"
        f"I am writing to express my strong interest in the {job_title} position at {company}. "
        f"With my background and skills, I am confident that I would be a valuable addition to your team.\n\n"
        f"Throughout my career, I have developed expertise in delivering high-quality results, "
        f"collaborating effectively across teams, and driving projects to successful completion. "
        f"I am particularly drawn to {company} because of its reputation for innovation and excellence.\n\n"
        f"I would welcome the opportunity to discuss how my experience and skills align with "
        f"the needs of {company}. Thank you for considering my application.\n\n"
        f"Best regards,\n{full_name}"
    )
