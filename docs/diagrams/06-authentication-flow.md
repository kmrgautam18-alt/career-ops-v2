# Authentication Flow Diagram

## Overview

The Authentication module handles user registration, login, token management, and session refresh in Career-Ops v2.

**Implemented features:**
- Argon2 Password Hashing
- JWT Access Token (30 min expiry)
- JWT Refresh Token (7 day expiry)
- Stateless Authentication
- Layered Architecture (Router → Service → Repository → DB)
- Custom Exception Handling

---

# Authentication Flow

```mermaid
flowchart LR

subgraph Client["👤 Client"]
    A["React Frontend / API Client"]
end

subgraph API["🌐 API Layer"]
    B["POST /api/v1/auth/login"]
    C["POST /api/v1/auth/refresh"]
end

subgraph Service["⚙️ Service Layer"]
    D["login_user()"]
    E["refresh_access_token()"]
end

subgraph Repository["🗄️ Repository Layer"]
    F["get_user_by_email()"]
end

subgraph Database["💾 Database"]
    G[("SQLite / PostgreSQL")]
end

subgraph Security["🔐 Security Layer"]
    H["Argon2 Password Verify"]
    I["JWT Access Token (30m)"]
    J["JWT Refresh Token (7d)"]
end

subgraph Response["📦 Response"]
    K["200 OK\n{access_token, refresh_token}"]
    L["401 Unauthorized"]
    M["403 Forbidden"]
end

A -->|"POST /login"| B
B --> D
D --> F
F --> G
G -->|"User Found"| H
G -.->|"User Not Found"| L
H -->|"Password Valid"| I
H -.->|"Invalid Password"| L
I --> J
J -->|"User Active"| K
J -.->|"Inactive User"| M
```

---

# Registration Flow

```mermaid
flowchart LR

    Client["👤 Client"]
    API["POST /api/v1/users/register"]
    Service["register_user()"]
    Repo["create_user()"]
    Security["Argon2 Hash Password"]
    DB[("Database")]
    Response["201 Created\nUser Profile"]

    Client --> API
    API --> Service
    Service -->|"Check duplicate email/username"| Repo
    Repo -->|"Check exists"| DB
    DB -->|"No duplicate"| Service
    Service --> Security
    Security --> Repo
    Repo --> DB
    DB --> Response
```

---

# Authentication Sequence

```mermaid
sequenceDiagram

actor Client
participant Router as FastAPI Router
participant Service as Auth Service
participant Repo as User Repository
participant DB as SQLite/PostgreSQL
participant Security as Argon2
participant JWT as JWT Utility

Client->>Router: POST /api/v1/auth/login

Router->>Service: login_user(email, password)
Service->>Repo: get_user_by_email()
Repo->>DB: SELECT user
DB-->>Repo: User Record
Repo-->>Service: User

Service->>Security: Verify Password

alt Invalid Password
    Security-->>Service: Failed
    Service-->>Router: InvalidCredentialsException
    Router-->>Client: HTTP 401
else Password Valid
    Security-->>Service: Success
    Service->>JWT: create_access_token(user_id, email, role)
    Service->>JWT: create_refresh_token(user_id)
    JWT-->>Service: JWT Tokens
    Service-->>Router: ApiResponse
    Router-->>Client: HTTP 200 (access_token, refresh_token)
end
```

---

# Architecture Layers

| Layer | Responsibility |
|-------|---------------|
| Client | Sends credentials, stores tokens in localStorage |
| API Layer | Routes: `/auth/login`, `/auth/refresh`, `/auth/logout`, `/users/register` |
| Service Layer | `login_user()`, `refresh_access_token()`, business logic |
| Repository Layer | `get_user_by_email()`, `create_user()` |
| Database | Persistent user storage (SQLite dev / PostgreSQL prod) |
| Security Layer | Argon2 password hashing, JWT generation/verification |
| Response Layer | Standardized `ApiResponse` envelope |

---

# Token Specifications

| Token | Lifetime | Payload | Storage |
|-------|----------|---------|---------|
| Access Token | 30 minutes | `sub` (user_id), `email`, `role`, `type`, `iat`, `exp`, `jti` | localStorage / Bearer header |
| Refresh Token | 7 days | `sub` (user_id), `type`, `iat`, `exp`, `jti` | localStorage (sent to /refresh) |

---

# HTTP Response Matrix

| Scenario | HTTP Status | Exception |
|----------|-------------|-----------|
| Login Successful | 200 | — |
| Invalid Credentials | 401 | `InvalidCredentialsException` |
| Expired Token | 401 | `UnauthorizedException` |
| Inactive User | 403 | `InactiveUserException` |
| User Not Found | 404 | `UserNotFoundException` |
| Duplicate Email | 409 | `DuplicateEmailException` |
| Duplicate Username | 409 | `DuplicateUsernameException` |

---

# Auth Module Status

| Feature | Status |
|---------|:------:|
| User Registration | ✅ |
| Login | ✅ |
| Argon2 Password Hashing | ✅ |
| JWT Access Token (30m) | ✅ |
| JWT Refresh Token (7d) | ✅ |
| Token Refresh | ✅ |
| Logout | ✅ |
| Exception Handling | ✅ |
| Stateless Authentication | ✅ |
| Layered Architecture | ✅ |
| RBAC (USER / ADMIN roles) | ✅ |
