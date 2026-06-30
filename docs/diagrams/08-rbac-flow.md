# Role-Based Access Control (RBAC)

## Overview

The RBAC module controls access to protected resources based on authenticated user roles.

Career-Ops follows a layered authorization model:

- Authentication (JWT)
- Authorization (RBAC)
- Business Logic
- Resource Access

---

# RBAC Architecture

```mermaid
flowchart LR

subgraph Client["👤 Client"]
    A["Authenticated User"]
end

subgraph Security["🔐 Security Layer"]
    B["Bearer Token"]
    C["JWT Validation"]
    D["Load Current User"]
    E{"Role Check"}
end

subgraph Roles["👥 Roles"]
    F["USER"]
    G["ADMIN"]
end

subgraph APIs["🌐 Protected APIs"]
    H["User APIs"]
    I["Admin APIs"]
end

subgraph Resources["💾 Resources"]
    J["Jobs"]
    K["Resume"]
    L["Applications"]
    M["System Administration"]
end

A --> B
B --> C
C --> D
D --> E

E -->|USER| F
E -->|ADMIN| G

F --> H
G --> I

H --> J
H --> K
H --> L

I --> J
I --> K
I --> L
I --> M
```

---

# Authorization Sequence

```mermaid
sequenceDiagram

actor Client

participant API as Protected API
participant Security as Security Dependency
participant JWT as JWT Utility
participant Repository as User Repository
participant DB as Database

Client->>API: Request with Bearer Token

API->>Security: get_current_active_user()

Security->>JWT: Decode JWT

JWT-->>Security: JWT Claims

Security->>Repository: Load User

Repository->>DB: SELECT User

DB-->>Repository: User

Repository-->>Security: User

Security->>Security: Validate Role

alt USER
    Security-->>API: Authorized
    API-->>Client: HTTP 200
else ADMIN
    Security-->>API: Authorized
    API-->>Client: HTTP 200
else Invalid Role
    Security-->>API: HTTP 403
    API-->>Client: Forbidden
end
```

---

# Current Roles

| Role | Description |
|------|-------------|
| USER | Standard authenticated user |
| ADMIN | Administrative user |

---

# Future Roles

The RBAC architecture is designed for future expansion.

Possible roles include:

- RECRUITER
- MODERATOR
- PREMIUM_USER
- SUPER_ADMIN

No architectural changes will be required to support additional roles.

---

# Security Pipeline

```text
Login
    │
JWT
    │
Bearer Token
    │
JWT Validation
    │
Current User
    │
Role Validation
    │
Protected API
```

---

# Sprint Status

| Feature | Status |
|---------|:------:|
| JWT Authentication | ✅ |
| Protected APIs | ✅ |
| Current User | ✅ |
| RBAC Foundation | 🔄 |
| Admin Authorization | ⏳ |
| Refresh Token Flow | ⏳ |

---

**Sprint:** Sprint 9.2 — Role-Based Access Control