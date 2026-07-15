# Authorization Flow Diagram

## Overview

The Authorization module validates every protected request using JWT and Role-Based Access Control (RBAC).

**Implemented:**
- JWT Bearer Authentication on all protected endpoints
- Three dependency levels: `get_current_user` → `get_current_active_user` → `get_current_admin_user`
- Token validation with python-jose
- Current user resolution from database
- Role enforcement (USER / ADMIN)

---

# Authorization Flow

```mermaid
flowchart LR

subgraph Client["👤 Client"]
    A["React Frontend"]
end

subgraph Nginx["🌐 Nginx"]
    N["Reverse Proxy\n/api/* → Backend"]
end

subgraph API["🌐 API Layer"]
    B["Protected Endpoint"]
end

subgraph Security["🔐 Security Dependencies"]
    C["get_current_user()"]
    D["get_current_active_user()"]
    E["get_current_admin_user()"]
end

subgraph JWT["🔑 JWT"]
    F["Extract Bearer Token"]
    G["Decode + Verify Signature"]
    H["Extract Claims\n{sub, email, role}"]
end

subgraph DB["💾 Database"]
    I[("SQLite / PostgreSQL")]
end

subgraph Response["📦 Response"]
    J["200 OK"]
    K["401 Unauthorized"]
    L["403 Forbidden"]
end

A --> N
N --> B
B --> C
C --> F
F --> G
G -->|Invalid| K
G -->|Valid| H
H -->|"Load user by ID"| I
I -->|"Return user"| D
D -->|"Check is_active"| E
E -->|"Check role=ADMIN"| J
D -->|"Active user"| J
E -->|"Not admin"| L
D -->|"Inactive"| L
```

---

# Authorization Sequence

```mermaid
sequenceDiagram

actor Client
participant API as Protected Endpoint
participant AuthDep as get_current_user()
participant ActiveDep as get_current_active_user()
participant AdminDep as get_current_admin_user()
participant JWT as JWT Utility
participant Repo as User Repository
participant DB as Database

Client->>API: GET /api/v1/jobs (Bearer token)

API->>AuthDep: Validate token
AuthDep->>JWT: decode_token(token)

alt Invalid Token
    JWT-->>AuthDep: JWTError
    AuthDep-->>API: UnauthorizedException
    API-->>Client: HTTP 401
else Valid Token
    JWT-->>AuthDep: {sub: 1, role: "ADMIN"}
    AuthDep->>Repo: get_user_by_id(1)
    Repo->>DB: SELECT * FROM users WHERE id=1
    DB-->>Repo: User {is_active: true, role: "ADMIN"}
    Repo-->>AuthDep: User
    AuthDep-->>ActiveDep: User
    
    ActiveDep->>ActiveDep: Check is_active
    alt Inactive
        ActiveDep-->>API: InactiveUserException
        API-->>Client: HTTP 403
    else Active
        ActiveDep-->>AdminDep: Active User
        
        AdminDep->>AdminDep: Check role == ADMIN
        alt Is Admin
            AdminDep-->>API: Authorized
            API-->>Client: HTTP 200
        else Not Admin
            AdminDep-->>API: ForbiddenException
            API-->>Client: HTTP 403
        end
    end
end
```

---

# Security Dependency Hierarchy

```mermaid
flowchart TD

    Public["✅ Public Endpoints\nGET /, POST /auth/login, POST /users/register"]
    Auth["🔐 get_current_user()\nDecodes JWT, loads user"]
    Active["🔐 get_current_active_user()\nChecks is_active flag"]
    Admin["🔐 get_current_admin_user()\nChecks role == ADMIN"]

    Public -->|"No auth required"| Route
    Auth -->|"Any authenticated"| Route
    Active -->|"Active users only"| Route
    Admin -->|"Admin only"| Route

    Route["API Router"]

    Route --> Jobs["/api/v1/jobs"]
    Route --> Apps["/api/v1/applications"]
    Route --> Resumes["/api/v1/resumes"]
    Route --> Dashboard["/api/v1/dashboard"]
    Route --> AI["/api/v1/ai"]
    Route --> Baserow["/api/v1/baserow"]
    Route --> AdminHealth["/api/v1/admin/health"]
```

---

# Security Pipeline

| Step | Function | Output |
|------|----------|--------|
| 1 | `oauth2_scheme` | Bearer token from header |
| 2 | `decode_token()` | JWT claims or `JWTError` |
| 3 | `get_user_by_id(sub)` | User object or `UnauthorizedException` |
| 4 | Check `is_active` | Active user or `InactiveUserException` |
| 5 | Check `role == ADMIN` | Admin user or `ForbiddenException` |
| 6 | Execute endpoint | HTTP 200 with data |

---

# Protected Endpoints

| Endpoint | Auth Required | Role Required |
|----------|---------------|---------------|
| `GET /api/v1/jobs` | ✅ Active User | — |
| `POST /api/v1/jobs` | ✅ Active User | — |
| `GET /api/v1/applications` | ✅ Active User | — |
| `POST /api/v1/resumes/upload` | ✅ Active User | — |
| `GET /api/v1/dashboard/` | ✅ Active User | — |
| `POST /api/v1/ai/ats-score` | ✅ Active User | — |
| `GET /api/v1/admin/health` | ✅ Active User | ADMIN |
| `GET /api/v1/baserow/health` | ✅ Active User | — |

---

# Auth Module Status

| Feature | Status |
|---------|:------:|
| JWT Token Validation | ✅ |
| `get_current_user()` Dependency | ✅ |
| `get_current_active_user()` Dependency | ✅ |
| `get_current_admin_user()` Dependency | ✅ |
| Protected Endpoints (all non-public routes) | ✅ |
| RBAC (USER / ADMIN) | ✅ |
| Custom Exceptions (401, 403, 404, 409) | ✅ |
