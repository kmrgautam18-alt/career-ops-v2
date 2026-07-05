from sqlalchemy.orm import Session

from backend.app.models.resume import Resume


def create_resume(
    db: Session,
    **kwargs,
) -> Resume:
    """
    Create a new resume.
    """

    resume = Resume(**kwargs)

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_resume_by_id(
    db: Session,
    resume_id: int,
) -> Resume | None:
    """
    Return a resume by its ID.
    """

    return db.query(Resume).filter(Resume.id == resume_id).first()


def get_resumes_by_user(
    db: Session,
    user_id: int,
) -> list[Resume]:
    """
    Return all resumes belonging to a user.
    """

    return (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.created_at.desc())
        .all()
    )


def get_resume_by_id_and_user(
    db: Session,
    resume_id: int,
    user_id: int,
) -> Resume | None:
    """
    Return a resume only if it belongs to the specified user.
    """

    return (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == user_id,
        )
        .first()
    )


def get_resume_file(
    db: Session,
    resume_id: int,
    user_id: int,
) -> Resume | None:
    """
    Return resume file metadata only if it belongs to the user.
    Used by download and preview endpoints.
    """

    return (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == user_id,
        )
        .first()
    )


def rename_resume(
    db: Session,
    resume: Resume,
    title: str,
) -> Resume:
    """
    Rename a resume title.
    """

    resume.title = title

    db.commit()
    db.refresh(resume)

    return resume


def update_resume(
    db: Session,
    resume: Resume,
) -> Resume:
    """
    Persist changes to an existing resume.
    """

    db.commit()
    db.refresh(resume)

    return resume


def delete_resume(
    db: Session,
    resume: Resume,
) -> None:
    """
    Delete a resume.
    """

    db.delete(resume)
    db.commit()
