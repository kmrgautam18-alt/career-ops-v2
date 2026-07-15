# Role-Based Access Control (RBAC)

## Overview

The RBAC module controls access to protected resources based on authenticated user roles and JWT claims.

**Implemented:**
- `get_current_user()` — JWT validation + user loading
- `get_current_active_user()` — Active status check
- `get_current_admin_user()` — Admin role enforcement
- Roles: USER, ADMIN

---

# RBAC Architecture

```mermaid
flowchart LR

subgraph Client["👤 Client"]
    A["Authenticated User\n(Bearer Token)"]
end

subgraph Security["🔐 Security Dependencies"]
    B["get_current_user()\nDecode JWT + load user"]
    C["get_current_active_user()\nCheck is_active flag"]
    D{"get_current_admin_user()\nCheck role == ADMIN"}
end

subgraph Roles["👥 Roles"]
    E["USER"]
    F["ADMIN"]
end

subgraph USER_APIs["🌐 USER Endpoints"]
    G["/api/v1/jobs/*"]
    H["/api/v1/applications/*"]
    I["/api/v1/resumes/*"]
    J["/api/v1/dashboard/*"]
    K["/api/v1/ai/*"]
    L["/api/v1/baserow/*"]
end

subgraph ADMIN_APIs["🌐 ADMIN Endpoints"]
    M["/api/v1/admin/health"]
end

subgraph Resources["💾 Resources"]
    N["Jobs · Applications · Resumes"]
    O["System Health · All Data"]
end

A --> B
B --> C

C -->|"USER role"| E
C -->|"ADMIN role"| F

E --> USER_APIs
F -->|"Also has USER access"| USER_APIs
F --> D
D -->|"Admin verified"| ADMIN_APIs

USER_APIs --> N
ADMIN_APIs --> O
```

---

# Role Permissions Matrix

| Endpoint | Public | USER | ADMIN |
|----------|:------:|:----:|:-----:|
| `GET /` | ✅ | — | — |
| `POST /users/register` | ✅ | — | — |
| `POST /auth/login` | ✅ | — | — |
| `POST /auth/refresh` | ✅ | — | — |
| `GET /users/me` | — | ✅ | ✅ |
| `GET/POST /jobs` | — | ✅ | ✅ |
| `GET/PATCH/DELETE /jobs/{id}` | — | ✅ (own) | ✅ |
| `GET/POST /applications` | — | ✅ | ✅ |
| `GET/POST /resumes` | — | ✅ | ✅ |
| `GET /dashboard` | — | ✅ | ✅ |
| `POST /ai/*` | — | ✅ | ✅ |
| `GET /admin/health` | — | — | ✅ |
| `GET /baserow/*` | — | ✅ | ✅ |

---

# Authorization Sequence

```mermaid
sequenceDiagram

actor Client
participant API as Protected API
participant Active as get_current_active_user()
participant Admin as get_current_admin_user()
participant JWT as JWT Utility
participant DB as Database

Client->>API: Request with Bearer Token

API->>Active: Validate & load user
Active->>JWT: decode_token(token)
JWT-->>Active: {sub: 1, role: "ADMIN"}

Active->>DB: get_user_by_id(1)
DB-->>Active: User(is_active=true, role="ADMIN")

Active->>Active: Check is_active == true
Note over Active: Active user authorized for USER endpoints

alt Admin endpoint requested
    Active-->>Admin: Pass user to admin check
    Admin->>Admin: Check role == "ADMIN"
    alt Is Admin
        Admin-->>API: Authorized for admin
        API-->>Client: HTTP 200
    else Not Admin
        Admin-->>API: ForbiddenException
        API-->>Client: HTTP 403
    end
else USER endpoint requested
    Active-->>API: Authorized as active user
    API-->>Client: HTTP 200
end
```

---

# Current Roles

| Role | Description | Can Access |
|------|-------------|------------|
| `USER` | Standard authenticated user | All data endpoints (own resources) |
| `ADMIN` | Administrative user | All USER endpoints + admin endpoints |

---

# Security Pipeline

```text
Request
  │
  ▼
OAuth2PasswordBearer (extract token from Authorization header)
  │
  ▼
get_current_user()
  ├── decode_token(token) → JWT claims
  ├── get_user_by_id(sub) → User object
  └── Returns user or raises UnauthorizedException
  │
  ▼
get_current_active_user()
  ├── Checks user.is_active == true
  └── Raises InactiveUserException if not
  │
  ▼
get_current_admin_user() [admin endpoints only]
  ├── Checks user.role == "ADMIN"
  └── Raises ForbiddenException if not
  │
  ▼
Endpoint executes with current_user injected
```

---

# RBAC Module Status

| Feature | Status |
|---------|:------:|
| JWT Authentication | ✅ |
| `get_current_user()` | ✅ |
| `get_current_active_user()` | ✅ |
| `get_current_admin_user()` | ✅ |
| Protected APIs (all non-public routes) | ✅ |
| User-resource ownership checks | ✅ |
| Custom 401/403 Exceptions | ✅ |
