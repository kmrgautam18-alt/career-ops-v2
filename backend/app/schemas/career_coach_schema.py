from pydantic import BaseModel


class CareerRoadmapRequest(BaseModel):
    current_role: str
    target_role: str
    experience_years: int
    skills: list[str] = []


class LearningPathRequest(BaseModel):
    goal: str
    current_skills: list[str] = []
    target_skills: list[str] = []
    weekly_hours: int = 5


class SkillGapRequest(BaseModel):
    resume_text: str
    target_role: str = ""


class ChatbotMessage(BaseModel):
    message: str
    context: str = ""


class CareerAdviceResponse(BaseModel):
    advice: str
    recommendations: list[str] = []
