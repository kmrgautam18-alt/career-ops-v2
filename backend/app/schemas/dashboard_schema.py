from pydantic import BaseModel, ConfigDict


class DashboardStats(BaseModel):
    """
    Dashboard statistics.
    """

    model_config = ConfigDict(from_attributes=True)

    total_jobs: int
    total_applications: int
    interviews: int
    offers: int
    rejections: int
    pending: int


class StatusCount(BaseModel):
    """
    Application status summary.
    """

    status: str
    count: int