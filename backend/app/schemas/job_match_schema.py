from pydantic import BaseModel, Field


class JobMatchRequest(BaseModel):
    """
    AI Job Match request with free-form profile and job details.
    """

    profile: str = Field(..., description="Candidate profile text (resume / background)")

    job_details: str = Field(..., description="Job posting details")


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

    classification: str = Field(default="moderate")

    skill: MatchComponentResponse | dict = Field(default_factory=dict)

    experience: MatchComponentResponse | dict = Field(default_factory=dict)

    education: MatchComponentResponse | dict = Field(default_factory=dict)

    certification: MatchComponentResponse | dict = Field(default_factory=dict)

    keyword: MatchComponentResponse | dict = Field(default_factory=dict)

    location: MatchComponentResponse | dict = Field(default_factory=dict)

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)