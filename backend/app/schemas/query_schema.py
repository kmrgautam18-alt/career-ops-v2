from enum import Enum


class SortField(str, Enum):  # noqa: UP042
    id = "id"
    company = "company"
    job_title = "title"
    status = "status"


class SortOrder(str, Enum):  # noqa: UP042
    asc = "asc"
    desc = "desc"
