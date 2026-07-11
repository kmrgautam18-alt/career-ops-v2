from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class OptimizationSuggestion:
    title: str
    current: str
    suggested: str
    priority: str = "MEDIUM"


@dataclass(slots=True)
class OptimizationReport:
    ats_score_before: float
    ats_score_after: float
    missing_keywords: list[str] = field(default_factory=list)
    suggestions: list[OptimizationSuggestion] = field(default_factory=list)