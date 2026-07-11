from pydantic import BaseModel, Field


class MatchComponentResponse(BaseModel):
    """
    Response for an individual matching component.
    """

    score: float = Field(..., ge=0, le=100)

    matched: list[str] = Field(default_factory=list)

    missing: list[str] = Field(default_factory=list)

    reasons: list[str] = Field(default_factory=list)


class JobMatchResponse(BaseModel):
    """
    Final AI Job Matching response.
    """

    overall_score: float = Field(..., ge=0, le=100)

    classification: str

    skill: MatchComponentResponse

    experience: MatchComponentResponse

    education: MatchComponentResponse

    certification: MatchComponentResponse

    keyword: MatchComponentResponse

    location: MatchComponentResponse

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)