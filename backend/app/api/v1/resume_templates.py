"""
Resume Template Marketplace API.
Users can create, share, browse, and use resume templates.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.models.auto_application import ResumeTemplate
from backend.app.schemas.common_schema import ApiResponse
from backend.app.security.dependencies import get_current_active_user

router = APIRouter(
    prefix="/resume-templates",
    tags=["Resume Templates"],
)


@router.get("/")
def list_templates(
    category: str | None = Query(None),
    search: str | None = Query(None),
    popular: bool = Query(False),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """List available resume templates, optionally filtered by category or search."""
    query = db.query(ResumeTemplate).filter(ResumeTemplate.is_public.is_(True))

    if category:
        query = query.filter(ResumeTemplate.category == category)
    if search:
        query = query.filter(ResumeTemplate.name.ilike(f"%{search}%"))
    if popular:
        query = query.order_by(ResumeTemplate.download_count.desc())

    total = query.count()
    templates = query.order_by(ResumeTemplate.created_at.desc()).limit(limit).offset(offset).all()

    return ApiResponse(
        success=True,
        message="Templates retrieved.",
        data={
            "templates": [
                {
                    "id": t.id,
                    "name": t.name,
                    "category": t.category,
                    "style": t.style,
                    "is_public": t.is_public,
                    "download_count": t.download_count or 0,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                }
                for t in templates
            ],
            "total": total,
        },
    )


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    """List all available template categories."""
    categories = (
        db.query(ResumeTemplate.category)
        .filter(ResumeTemplate.is_public.is_(True), ResumeTemplate.category.isnot(None))
        .distinct()
        .all()
    )
    return ApiResponse(
        success=True,
        message="Categories retrieved.",
        data=[c[0] for c in categories if c[0]],
    )


@router.get("/{template_id}")
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific template by ID."""
    template = db.get(ResumeTemplate, template_id)
    if template is None:
        raise HTTPException(404, "Template not found.")

    # Increment download count
    template.download_count = (template.download_count or 0) + 1
    db.commit()

    return ApiResponse(
        success=True,
        message="Template retrieved.",
        data={
            "id": template.id,
            "name": template.name,
            "category": template.category,
            "style": template.style,
            "content": template.content,
            "is_public": template.is_public,
            "download_count": template.download_count or 0,
            "created_at": template.created_at.isoformat() if template.created_at else None,
        },
    )


@router.post("/")
def create_template(
    name: str,
    content: str,
    category: str = "general",
    style: str = "modern",
    is_public: bool = False,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Create a new resume template."""
    template = ResumeTemplate(
        user_id=current_user.id,
        name=name,
        category=category,
        style=style,
        content=content,
        is_public=is_public,
    )
    db.add(template)
    db.commit()
    db.refresh(template)

    return ApiResponse(
        success=True,
        message="Template created.",
        data={"id": template.id, "name": template.name, "category": template.category},
    )


@router.put("/{template_id}")
def update_template(
    template_id: int,
    name: str | None = None,
    content: str | None = None,
    category: str | None = None,
    style: str | None = None,
    is_public: bool | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Update a template (only owner can update)."""
    template = db.get(ResumeTemplate, template_id)
    if template is None:
        raise HTTPException(404, "Template not found.")
    if template.user_id != current_user.id:
        raise HTTPException(403, "Only the owner can update this template.")

    if name is not None:
        template.name = name
    if content is not None:
        template.content = content
    if category is not None:
        template.category = category
    if style is not None:
        template.style = style
    if is_public is not None:
        template.is_public = is_public

    db.commit()
    return ApiResponse(success=True, message="Template updated.")


@router.delete("/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Delete a template (only owner can delete)."""
    template = db.get(ResumeTemplate, template_id)
    if template is None:
        raise HTTPException(404, "Template not found.")
    if template.user_id != current_user.id:
        raise HTTPException(403, "Only the owner can delete this template.")

    db.delete(template)
    db.commit()
    return ApiResponse(success=True, message="Template deleted.")


@router.get("/my/")
def my_templates(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """List templates created by the current user."""
    templates = (
        db.query(ResumeTemplate)
        .filter(ResumeTemplate.user_id == current_user.id)
        .order_by(ResumeTemplate.created_at.desc())
        .all()
    )

    return ApiResponse(
        success=True,
        message="Your templates retrieved.",
        data=[
            {
                "id": t.id,
                "name": t.name,
                "category": t.category,
                "style": t.style,
                "is_public": t.is_public,
                "download_count": t.download_count or 0,
            }
            for t in templates
        ],
    )
