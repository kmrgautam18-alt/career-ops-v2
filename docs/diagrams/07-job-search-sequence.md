# Job Search Sequence Diagram

Version: 2.0

Status: Active

---

# Purpose

This sequence diagram illustrates how a job search request flows through the Career-Ops v2 backend with full filtering, sorting, and pagination.

---

# Sequence Diagram

```mermaid
sequenceDiagram

actor User
participant Browser as React Frontend
participant Nginx
participant Router as FastAPI Router
participant Service as Job Service
participant Repo as Job Repository
participant DB as SQLite/PostgreSQL

User->>Browser: Types "engineer" in search bar
Browser->>Nginx: GET /api/v1/jobs?search=engineer&status=saved&sort=-created_at&page=1&size=20
Nginx->>Router: Proxy to backend:8000
Router->>Router: Validate params (Pydantic)
Router->>Service: list_jobs(current_user, search="engineer", status="saved", sort="-created_at", page=1, size=20)
Service->>Repo: get_jobs_paginated(user_id=1, search="engineer", filters={status: "saved"}, sort={created_at: desc}, page=1, size=20)
Repo->>DB: SELECT * FROM jobs WHERE user_id=1 AND status='saved' AND (title LIKE '%engineer%' OR company LIKE '%engineer%') ORDER BY created_at DESC LIMIT 20 OFFSET 0
DB-->>Repo: 5 matching jobs
Repo-->>Service: [Job, Job, Job, Job, Job] + total_count=5
Service-->>Router: ApiResponse{success: true, data: [...], pagination: {page: 1, size: 20, total: 5, total_pages: 1}}
Router-->>Nginx: JSON Response
Nginx-->>Browser: JSON Response
Browser-->>User: Display 5 job cards with status badges
```

---

# Search & Filter Options

| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| `search` | string | `engineer` | Full-text search on title + company |
| `status` | string | `saved` | Filter by status: saved, applied, interviewing, offer, rejected, accepted |
| `company` | string | `Google` | Filter by company name |
| `sort` | string | `-created_at` | Sort field (+ for asc, - for desc) |
| `page` | integer | `1` | Page number (1-indexed) |
| `size` | integer | `20` | Items per page (default: 20) |

---

# Job Status Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Saved
    Saved --> Applied
    Applied --> Interviewing
    Interviewing --> Offer
    Offer --> Accepted
    Offer --> Rejected
    Interviewing --> Rejected
    Applied --> Rejected
```

---

# Flow Description

1. User types a search query in the React frontend
2. Frontend sends GET request with query params through Nginx proxy
3. FastAPI Router validates all parameters via Pydantic schemas
4. Service Layer applies business logic (ownership, permissions)
5. Repository constructs SQL query with search, filter, sort, and pagination
6. Database returns matching job records
7. Response is wrapped in standardized `ApiResponse` with pagination metadata

---

# Current Search Fields

- Title (LIKE search)
- Company (LIKE search)
- Status (exact match)
- Combined: title + company across all statuses

---

# Engineering Principles

- Repository owns all SQL queries
- Service owns business logic (ownership validation)
- Router owns HTTP (param validation via Pydantic)
- All responses use `ApiResponse` envelope
- Search is pagination-aware with total counts
- Filtering uses query parameters, not path parameters
