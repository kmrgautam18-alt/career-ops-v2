from enum import Enum


class SortField(str, Enum):
    id = "id"
    company = "company"
    job_title = "title"
    status = "status"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"
