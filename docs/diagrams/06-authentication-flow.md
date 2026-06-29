# Authentication Flow Diagram

## Overview

The Authentication module is responsible for securely authenticating users in Career-Ops v2.

It uses modern authentication standards including:

* Argon2 Password Hashing
* JWT Access Token
* JWT Refresh Token
* Stateless Authentication
* Layered Architecture
* Custom Exception Handling

---

# Authentication Flow

```mermaid
flowchart LR

subgraph Client["👤 Client"]
    A["Web / Mobile Client"]
end

subgraph API["🌐 API Layer"]
    B["FastAPI Router<br/>POST /api/v1/auth/login"]
end

subgraph Service["⚙️ Service Layer"]
    C["Auth Service<br/>login_user()"]
end

subgraph Repository["🗄️ Repository Layer"]
    D["User Repository<br/>get_user_by_email()"]
end

subgraph Database["💾 Database"]
    E[("SQLite")]
end

subgraph Security["🔐 Security Layer"]
    F["Argon2 Password Verification"]
    G["JWT Generator"]
end

subgraph Response["📦 Response"]
    H["200 OK<br/>Access Token<br/>Refresh Token"]
    I["401 Unauthorized"]
    J["403 Forbidden"]
end

A -->|"POST /login"| B
B --> C
C --> D
D --> E

E -->|"User Found"| F
E -.->|"User Not Found"| I

F -->|"Password Valid"| G
F -.->|"Invalid Password"| I

G -->|"User Active"| H
G -.->|"Inactive User"| J
```

---

# Authentication Sequence

```mermaid
sequenceDiagram

actor Client

participant Router as FastAPI Router
participant Service as Auth Service
participant Repo as User Repository
participant DB as SQLite
participant Security as Argon2
participant JWT as JWT Utility

Client->>Router: POST /api/v1/auth/login

Router->>Service: login_user(email,password)

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

    Service->>JWT: create_access_token()

    Service->>JWT: create_refresh_token()

    JWT-->>Service: JWT Tokens

    Service-->>Router: ApiResponse

    Router-->>Client: HTTP 200
end
```

---

# Architecture Layers

| Layer            | Responsibility                         |
| ---------------- | -------------------------------------- |
| Client           | Sends authentication request           |
| API Layer        | Accepts HTTP request                   |
| Service Layer    | Authentication business logic          |
| Repository Layer | User retrieval                         |
| Database         | Persistent user storage                |
| Security Layer   | Password verification & JWT generation |
| Response Layer   | Standard API response                  |

---

# Security Components

| Component         | Purpose                         |
| ----------------- | ------------------------------- |
| Argon2            | Password Hashing & Verification |
| JWT               | Stateless Authentication        |
| Access Token      | API Authentication              |
| Refresh Token     | Token Renewal                   |
| Custom Exceptions | Secure error handling           |

---

# HTTP Response Matrix

| Scenario            | HTTP Status |
| ------------------- | ----------: |
| Login Successful    |         200 |
| Invalid Credentials |         401 |
| Unauthorized Token  |         401 |
| Inactive User       |         403 |
| User Not Found      |         404 |
| Duplicate Email     |         409 |
| Duplicate Username  |         409 |

---

# Authentication Module Status

| Feature                  | Status |
| ------------------------ | :----: |
| User Registration        |    ✅   |
| Login                    |    ✅   |
| Argon2 Password Hashing  |    ✅   |
| JWT Access Token         |    ✅   |
| JWT Refresh Token        |    ✅   |
| Exception Handling       |    ✅   |
| Stateless Authentication |    ✅   |
| Layered Architecture     |    ✅   |

---

**Version:** Authentication Module v1.0
**Sprint:** Sprint 8.2 — Authentication Module
