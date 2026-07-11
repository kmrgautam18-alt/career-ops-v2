from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

CompanyStr = Annotated[
    str,
    Field(
        min_length=2,
        max_length=100,
        strip_whitespace=True,
        description="Company name",
    ),
]

TitleStr = Annotated[
    str,
    Field(
        min_length=2,
        max_length=150,
        strip_whitespace=True,
        description="Job title",
    ),
]

DescriptionStr = Annotated[
    str | None,
    Field(
        default=None,
        description="Complete job description",
    ),
]


class JobCreate(BaseModel):
    company: CompanyStr
    title: TitleStr
    url: HttpUrl
    description: DescriptionStr = None


class JobUpdate(BaseModel):
    company: CompanyStr
    title: TitleStr
    url: HttpUrl
    description: DescriptionStr = None


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    title: str
    url: str
    description: str | None = None
    status: str