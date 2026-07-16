from pydantic import BaseModel


class InterviewRequest(BaseModel):
    job_title: str = ""
    company: str = ""
    skills: list[str] = []
    difficulty: str = "medium"


class InterviewQuestionResponse(BaseModel):
    question: str
    category: str
    difficulty: str


class InterviewResponse(BaseModel):
    questions: list[InterviewQuestionResponse]
