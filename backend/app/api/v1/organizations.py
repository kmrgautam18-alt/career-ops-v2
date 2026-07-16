"""Organizations / Multi-Tenant API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.models.organization import Organization, OrganizationMember
from backend.app.schemas.common_schema import ApiResponse
from backend.app.security.dependencies import get_current_active_user

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post("/")
def create_organization(
    name: str,
    slug: str,
    description: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Create a new organization."""
    existing = db.query(Organization).filter(Organization.slug == slug).first()
    if existing:
        raise HTTPException(400, "Organization slug already exists.")

    org = Organization(
        name=name,
        slug=slug,
        description=description,
        owner_id=current_user.id,
    )
    db.add(org)
    db.flush()

    # Add creator as owner member
    member = OrganizationMember(
        organization_id=org.id,
        user_id=current_user.id,
        role="owner",
    )
    db.add(member)
    db.commit()
    db.refresh(org)

    return ApiResponse(success=True, message="Organization created.", data={
        "id": org.id, "name": org.name, "slug": org.slug, "owner_id": org.owner_id,
    })


@router.get("/")
def list_organizations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """List organizations the current user belongs to."""
    memberships = db.query(OrganizationMember).filter(
        OrganizationMember.user_id == current_user.id,
        OrganizationMember.is_active == True,
    ).all()

    org_ids = [m.organization_id for m in memberships]
    orgs = db.query(Organization).filter(Organization.id.in_(org_ids)).all()

    return ApiResponse(success=True, message="Organizations retrieved.", data=[
        {"id": o.id, "name": o.name, "slug": o.slug, "description": o.description,
         "max_members": o.max_members, "is_active": o.is_active}
        for o in orgs
    ])


@router.get("/{org_id}/members")
def list_members(
    org_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """List members of an organization."""
    members = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == org_id,
        OrganizationMember.is_active == True,
    ).all()

    return ApiResponse(success=True, message="Members retrieved.", data=[
        {"id": m.id, "user_id": m.user_id, "role": m.role, "joined_at": str(m.joined_at)}
        for m in members
    ])


@router.post("/{org_id}/invite")
def invite_member(
    org_id: int,
    user_id: int,
    role: str = "member",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Invite a user to an organization."""
    org = db.get(Organization, org_id)
    if not org:
        raise HTTPException(404, "Organization not found.")

    if org.owner_id != current_user.id:
        raise HTTPException(403, "Only the owner can invite members.")

    existing = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == org_id,
        OrganizationMember.user_id == user_id,
    ).first()
    if existing:
        raise HTTPException(400, "User is already a member.")

    member = OrganizationMember(
        organization_id=org_id,
        user_id=user_id,
        role=role,
    )
    db.add(member)
    db.commit()

    return ApiResponse(success=True, message="Member invited.", data=None)
