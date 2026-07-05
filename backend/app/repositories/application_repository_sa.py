from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.application import Application


def create_application(
    db: Session,
    user_id: int,
    job_id: int,
    applied_date: date,
    status: str,
    notes: str | None,
) -> Application:
    """
    Create a new application.
    """

    application = Application(
        user_id=user_id,
        job_id=job_id,
        applied_date=applied_date,
        status=status,
        notes=notes,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_application_by_id(
    db: Session,
    application_id: int,
) -> Application | None:
    """
    Return an application by its ID.
    """

    return db.get(
        Application,
        application_id,
    )


def get_applications_by_user(
    db: Session,
    user_id: int,
) -> list[Application]:
    """
    Return all applications belonging to a user.
    """

    return (
        db.scalars(
            select(Application)
            .where(
                Application.user_id == user_id,
            )
            .order_by(
                Application.created_at.desc(),
            )
        )
        .all()
    )


def get_application_by_user_and_job(
    db: Session,
    user_id: int,
    job_id: int,
) -> Application | None:
    """
    Return an application for a specific user and job.
    """

    return db.scalar(
        select(Application).where(
            Application.user_id == user_id,
            Application.job_id == job_id,
        )
    )


def get_application_by_id_and_user(
    db: Session,
    application_id: int,
    user_id: int,
) -> Application | None:
    """
    Return an application only if it belongs to the user.
    """

    return db.scalar(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user_id,
        )
    )


def update_application(
    db: Session,
    application: Application,
) -> Application:
    """
    Persist changes to an existing application.
    """

    db.commit()
    db.refresh(application)

    return application


def delete_application(
    db: Session,
    application: Application,
) -> None:
    """
    Delete an application.
    """

    db.delete(application)
    db.commit()