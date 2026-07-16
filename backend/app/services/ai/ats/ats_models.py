from dataclasses import dataclass, field


@dataclass(slots=True)
class ATSScoreBreakdown:
    keywords: float = 0.0
    formatting: float = 0.0
    sections: float = 0.0
    readability: float = 0.0
    overall: float = 0.0


@dataclass(slots=True)
class ATSRecommendation:
    title: str
    description: str
    priority: str = "MEDIUM"


@dataclass(slots=True)
class ATSReport:
    score: ATSScoreBreakdown
    recommendations: list[ATSRecommendation] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)