from pydantic import BaseModel


class JobResponse(BaseModel):
    id: int
    company: str
    title: str
    status: str
