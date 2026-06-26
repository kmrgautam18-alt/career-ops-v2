from pydantic import BaseModel, Field

class JobCreate(BaseModel):
    company: str = Field(..., min_length=2, max_length=100)
    title: str = Field(..., min_length=2, max_length=150)
    url: str = Field(..., min_length=5)

class JobResponse(BaseModel):
    id: int
    company: str
    title: str
    status: str
