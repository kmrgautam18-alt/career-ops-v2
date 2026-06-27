from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    company: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    status: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
