from pydantic import BaseModel, ConfigDict


class DashboardStats(BaseModel):
    """
    Overall dashboard statistics.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    total_jobs: int
    total_applications: int
    total_resumes: int

    applied: int
    interviews: int
    offers: int
    rejections: int


class StatusCount(BaseModel):
    """
    Application status summary.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    status: str
    count: int