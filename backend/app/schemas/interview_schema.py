from pydantic import BaseModel


class InterviewRequest(BaseModel):
    skills: list[str]
    difficulty: str = "All"


class InterviewQuestionResponse(BaseModel):
    question: str
    category: str
    difficulty: str


class InterviewResponse(BaseModel):
    questions: list[InterviewQuestionResponse]