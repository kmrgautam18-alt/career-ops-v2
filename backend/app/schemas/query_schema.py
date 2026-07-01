from enum import StrEnum


class SortField(StrEnum):
    id = "id"
    company = "company"
    job_title = "title"
    status = "status"


class SortOrder(StrEnum):
    asc = "asc"
    desc = "desc"