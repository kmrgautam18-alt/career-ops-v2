from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.application import Application


def create_application(
    db: Session,
    *,
    user_id: int,
    job_id: int,
    status: str = "Applied",
    applied_date,
    notes: str | None = None,
) -> Application:
    """
    Create a new job application.
    """

    application = Application(
        user_id=user_id,
        job_id=job_id,
        status=status,
        applied_date=applied_date,
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
    Return application by id.
    """

    return db.get(
        Application,
        application_id,
    )

def get_application_by_id_and_user(
    db: Session,
    application_id: int,
    user_id: int,
) -> Application | None:
    """
    Return an application owned by a user.
    """

    return db.scalar(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user_id,
        )
    )


def get_application_by_user_and_job(
    db: Session,
    user_id: int,
    job_id: int,
) -> Application | None:
    """
    Return application by user and job.
    """

    return db.scalar(
        select(Application).where(
            Application.user_id == user_id,
            Application.job_id == job_id,
        )
    )


def get_applications_by_user(
    db: Session,
    user_id: int,
) -> list[Application]:
    """
    Return all applications for a user.
    """

    return list(
        db.scalars(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.applied_date.desc())
        ).all()
    )


def get_user_applications(
    db: Session,
    user_id: int,
) -> list[Application]:
    """
    Return all applications for a user.
    """

    return list(
        db.scalars(
            select(Application)
            .where(
                Application.user_id == user_id,
            )
            .order_by(
                Application.applied_date.desc(),
            )
        ).all()
    )


def get_application_count(
    db: Session,
    user_id: int,
) -> int:
    """
    Return total application count.
    """

    return (
        db.scalar(
            select(func.count())
            .select_from(Application)
            .where(
                Application.user_id == user_id,
            )
        )
        or 0
    )


def delete_application(
    db: Session,
    application: Application,
) -> None:
    """
    Delete application.
    """

    db.delete(application)
    db.commit()


def update_application(
    db: Session,
    application: Application,
) -> Application:
    """
    Persist application changes.
    """

    db.commit()
    db.refresh(application)

    return application