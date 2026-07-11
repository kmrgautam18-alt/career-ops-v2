from pydantic import BaseModel


class ATSRequest(BaseModel):
    resume_text: str
    required_keywords: list[str]


class ATSRecommendationResponse(BaseModel):
    title: str
    description: str
    priority: str


class ATSScoreResponse(BaseModel):
    keywords: float
    formatting: float
    sections: float
    readability: float
    overall: float


class ATSResponse(BaseModel):
    score: ATSScoreResponse
    recommendations: list[ATSRecommendationResponse]

class ResumeOptimizerRequest(BaseModel):
    resume_text: str
    required_keywords: list[str]

class ResumeOptimizerResponse(BaseModel):
    ats_score_before: float
    ats_score_after: float
    missing_keywords: list[str]
    suggestions: list[str]