from dataclasses import dataclass, field


@dataclass(slots=True)
class InterviewQuestion:
    question: str
    category: str
    difficulty: str


@dataclass(slots=True)
class InterviewReport:
    questions: list[InterviewQuestion] = field(default_factory=list)