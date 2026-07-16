"""
Baserow REST API Service

Provides a Python client to interact with Baserow (open-source Airtable alternative)
databases from within the Career-Ops backend.

Endpoints:
    GET    /api/database/rows/table/{table_id}/       → List rows
    POST   /api/database/rows/table/{table_id}/       → Create row
    PATCH  /api/database/rows/table/{table_id}/{row_id}/  → Update row
    DELETE /api/database/rows/table/{table_id}/{row_id}/  → Delete row
    GET    /api/database/tables/database/{database_id}/ → List tables

Requires:
    BASEROW_URL   — e.g. "https://api.baserow.io" (or self-hosted URL)
    BASEROW_TOKEN — API token from Baserow settings
"""

from dataclasses import dataclass
from typing import Any

import requests

from backend.app.core.config import settings


@dataclass
class BaserowConfig:
    """Connection configuration for a Baserow instance."""

    base_url: str
    token: str

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }


class BaserowService:
    """
    Lightweight client for the Baserow REST API.
    """

    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
    ) -> None:
        self.config = BaserowConfig(
            base_url=(base_url or settings.BASEROW_URL).rstrip("/"),
            token=token or settings.BASEROW_TOKEN,
        )

    # ------------------------------------------------------------------
    # Tables
    # ------------------------------------------------------------------

    def list_tables(
        self,
        database_id: int,
    ) -> list[dict[str, Any]]:
        """
        Retrieve all tables belonging to a database.
        """
        resp = requests.get(
            f"{self.config.base_url}/api/database/tables/database/{database_id}/",
            headers=self.config.headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    # ------------------------------------------------------------------
    # Rows
    # ------------------------------------------------------------------

    def list_rows(
        self,
        table_id: int,
        *,
        page: int = 1,
        size: int = 100,
        search: str = "",
        order_by: str = "",
    ) -> dict[str, Any]:
        """
        Paginated list of rows from a table.

        Returns a dict with keys: ``count``, ``next``, ``previous``, ``results``.
        """
        params: dict[str, Any] = {"page": page, "size": size}
        if search:
            params["search"] = search
        if order_by:
            params["order_by"] = order_by

        resp = requests.get(
            f"{self.config.base_url}/api/database/rows/table/{table_id}/",
            headers=self.config.headers,
            params=params,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def get_row(
        self,
        table_id: int,
        row_id: int,
    ) -> dict[str, Any]:
        """
        Retrieve a single row by ID.
        """
        resp = requests.get(
            f"{self.config.base_url}/api/database/rows/table/{table_id}/{row_id}/",
            headers=self.config.headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def create_row(
        self,
        table_id: int,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Insert a new row into a table.

        Field keys must use the ``field_{id}`` naming convention.
        """
        resp = requests.post(
            f"{self.config.base_url}/api/database/rows/table/{table_id}/",
            headers=self.config.headers,
            json=data,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def update_row(
        self,
        table_id: int,
        row_id: int,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Partially update an existing row.
        """
        resp = requests.patch(
            f"{self.config.base_url}/api/database/rows/table/{table_id}/{row_id}/",
            headers=self.config.headers,
            json=data,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()  # type: ignore[no-any-return]

    def delete_row(
        self,
        table_id: int,
        row_id: int,
    ) -> None:
        """
        Delete a row by ID.
        """
        resp = requests.delete(
            f"{self.config.base_url}/api/database/rows/table/{table_id}/{row_id}/",
            headers=self.config.headers,
            timeout=30,
        )
        resp.raise_for_status()

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def check_connection(self) -> bool:
        """
        Verify that the Baserow instance is reachable and the token is valid
        by fetching user info.
        """
        try:
            resp = requests.get(
                f"{self.config.base_url}/api/user/",
                headers=self.config.headers,
                timeout=15,
            )
            return resp.status_code == 200
        except requests.RequestException:
            return False


# Singleton for easy reuse
baserow = BaserowService()
