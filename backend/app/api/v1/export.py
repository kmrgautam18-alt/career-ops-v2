"""
Data Export endpoints — GDPR-compliant user data portability.
"""

import csv
import io
import json
import logging
from typing import Literal

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.export_service import export_user_data_csv, export_user_data_json

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/export",
    tags=["Data Export"],
)


@router.get("/json")
def export_json(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Export all user data as JSON."""
    data = export_user_data_json(db, current_user)
    return Response(
        content=json.dumps(data, indent=2, default=str),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=careerops-export-{current_user.id}.json"},
    )


@router.get("/csv")
def export_csv(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Export all user data as a CSV zip file."""
    csv_data = export_user_data_csv(db, current_user)

    # If multiple tables, return as combined text with separators
    output = io.StringIO()
    for table_name, content in csv_data.items():
        output.write(f"\n--- {table_name} ---\n")
        output.write(content)
        output.write("\n")

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=careerops-export-{current_user.id}.csv"},
    )
