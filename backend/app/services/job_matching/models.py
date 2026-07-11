from dataclasses import dataclass, field


@dataclass(slots=True)
class MatchComponent:
    """
    Represents the result of a single matching component.
    """

    score: float
    matched: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MatchResult:
    """
    Final job matching result.
    """

    overall_score: float

    skill: MatchComponent

    experience: MatchComponent

    education: MatchComponent

    certification: MatchComponent

    keyword: MatchComponent

    location: MatchComponent

    classification: str

    strengths: list[str] = field(default_factory=list)

    weaknesses: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)