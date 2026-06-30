# Authorization Flow Diagram

## Overview

The Authorization module validates every protected request using JWT authentication before allowing access to business resources.

This module provides:

* JWT Bearer Authentication
* Token Validation
* Current User Resolution
* Role-Based Access Control (RBAC) Foundation
* Protected API Access

---

# Authorization Flow

```mermaid
flowchart LR

subgraph Client["👤 Client"]
    A["Web / Mobile Client"]
end

subgraph API["🌐 API Layer"]
    B["Protected API Endpoint"]
end

subgraph Security["🔐 Security Layer"]
    C["Authorization Header"]
    D["Extract Bearer Token"]
    E["Verify JWT Signature"]
    F["Decode JWT Claims"]
    G["Load Current User"]
    H["Verify User Status"]
end

subgraph Database["💾 Database"]
    I[("SQLite")]
end

subgraph Response["📦 Response"]
    J["200 OK"]
    K["401 Unauthorized"]
    L["403 Forbidden"]
end

A -->|"Authorization: Bearer JWT"| B

B --> C

C --> D

D --> E

E -->|"Invalid Token"| K

E -->|"Valid Token"| F

F --> G

G --> I

I --> H

H -->|"Inactive User"| L

H -->|"Authorized"| J
```

---

# Authorization Sequence

```mermaid
sequenceDiagram

actor Client

participant API as Protected API
participant Dependency as get_current_user()
participant JWT as JWT Utility
participant Repository as User Repository
participant Database as SQLite

Client->>API: GET /protected-resource

API->>Dependency: Validate Bearer Token

Dependency->>JWT: Decode JWT

alt Invalid Token

JWT-->>Dependency: Invalid

Dependency-->>API: UnauthorizedException

API-->>Client: HTTP 401

else Valid Token

JWT-->>Dependency: JWT Claims

Dependency->>Repository: get_user_by_id()

Repository->>Database: SELECT User

Database-->>Repository: User

Repository-->>Dependency: User

Dependency-->>API: Current User

API-->>Client: HTTP 200

end
```

---

# Security Pipeline

| Step | Description             |
| ---- | ----------------------- |
| 1    | Receive Bearer Token    |
| 2    | Verify JWT Signature    |
| 3    | Decode JWT Claims       |
| 4    | Load User from Database |
| 5    | Validate Active Status  |
| 6    | Return Current User     |
| 7    | Execute Protected API   |

---

# Future Expansion

This authorization framework will secure:

* User APIs
* Resume APIs
* Job APIs
* AI Services
* Admin APIs
* n8n APIs

---

# Sprint Status

| Feature                  | Status |
| ------------------------ | :----: |
| JWT Validation           |    ⏳   |
| Current User Dependency  |    ⏳   |
| Protected Endpoints      |    ⏳   |
| RBAC Foundation          |    ⏳   |
| Authorization Middleware |    ⏳   |

---

**Sprint:** Sprint 9 — Authorization & Security Foundation
