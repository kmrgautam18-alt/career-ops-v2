"""
Module 13 — AI Content Generation
Cover Letter, HR Email, Follow-up, Thank You, Salary Negotiation, Referral, LinkedIn
"""
import random

from fastapi import APIRouter, Depends

from backend.app.security.dependencies import get_current_active_user

router = APIRouter(prefix="/ai/content", tags=["AI Content"])


_TEMPLATES = {
    "cover_letter": """Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With my background in {field} and experience in {skills}, I am confident that my skills align perfectly with your requirements.

Throughout my career, I have {achievement}. I am particularly excited about {company}'s work in {industry} and would love to contribute to your team.

Thank you for considering my application. I look forward to the opportunity to discuss how I can add value to {company}.

Best regards,
{name}""",

    "follow_up": """Subject: Following Up on {job_title} Application

Dear {hiring_manager},

I hope this message finds you well. I am writing to follow up on my application for the {job_title} position at {company}, which I submitted on {date}.

I remain very enthusiastic about this opportunity and believe my experience in {skills} would make me a strong contributor to your team.

Please let me know if there are any updates regarding my application status.

Best regards,
{name}""",

    "thank_you": """Subject: Thank You — {job_title} Interview

Dear {interviewer},

Thank you so much for taking the time to speak with me today about the {job_title} role at {company}. I truly enjoyed learning more about the team and the exciting work you are doing.

Our conversation reinforced my interest in this position, particularly regarding {topic}. I am confident that my experience in {skills} would allow me to contribute immediately.

Please feel free to reach out if you need any additional information.

Best regards,
{name}""",

    "salary_negotiation": """Subject: Offer Discussion — {job_title} Position

Dear {hiring_manager},

Thank you for extending the offer for the {job_title} position at {company}. I am very excited about this opportunity and believe I would be a great fit for the team.

Based on my research into market rates for this role in {location}, as well as my {experience_years} years of experience in {field}, I was hoping we could discuss the compensation package. I was looking for a base salary in the range of {desired_salary}.

I am confident that we can find a mutually beneficial arrangement and look forward to continuing our discussions.

Best regards,
{name}""",

    "referral_request": """Subject: Referral Request — {job_title} at {company}

Hi {connection},

I hope you're doing well! I noticed that {company} is hiring for a {job_title} position, and I think I would be a great fit given my background in {field}.

If you're comfortable, I would really appreciate a referral. I've attached my resume for your reference.

Thanks so much for considering!

Best,
{name}""",

    "linkedin_post": """I'm excited to share that I've just accepted a new role as {job_title} at {company}! 🎉

After an incredible journey at {previous_company}, I'm ready for this next chapter. I want to thank everyone who has supported me along the way.

I'm looking forward to contributing to {company}'s mission of {mission}. If you're interested in connecting or learning more about opportunities at {company}, feel free to reach out!

#NewJob #Career #Tech #Opportunity""",
}


@router.post("/generate")
def generate_content(
    content_type: str = "cover_letter",
    variables: dict = {},
    current_user=Depends(get_current_active_user),
):
    template = _TEMPLATES.get(content_type)
    if not template:
        return {"success": False, "message": f"Unknown content type: {content_type}. Available: {', '.join(_TEMPLATES.keys())}"}

    filled = template
    for key, value in variables.items():
        placeholder = "{" + key + "}"
        filled = filled.replace(placeholder, str(value))

    return {
        "success": True,
        "data": {
            "type": content_type,
            "content": filled,
            "word_count": len(filled.split()),
        },
    }


@router.get("/templates")
def list_templates(current_user=Depends(get_current_active_user)):
    return {
        "success": True,
        "data": [
            {"id": k, "name": k.replace("_", " ").title(), "variables": _infer_variables(k)}
            for k in _TEMPLATES.keys()
        ],
    }


def _infer_variables(template_key: str) -> list[str]:
    return ["name", "company", "job_title"]
