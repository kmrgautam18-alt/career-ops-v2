# Refresh Token Flow

## Overview

The Refresh Token module allows clients to obtain a new Access Token without requiring the user to log in again. The Axios interceptor on the frontend handles this automatically when a 401 response is received.

**Implemented:**
- Access Token: 30 minutes
- Refresh Token: 7 days
- Automatic refresh via Axios interceptor
- JWT signature verification on every request

---

# Authentication Lifecycle

```mermaid
flowchart LR

subgraph Client["👤 Client"]
    A["Login"]
    B["Store Tokens\nlocalStorage"]
    C["API Request\nwith Access Token"]
    D["401 Received\nToken Expired"]
    E["Auto-Refresh\nvia Axios Interceptor"]
end

subgraph Backend["🚀 Backend"]
    F["POST /api/v1/auth/login"]
    G["POST /api/v1/auth/refresh"]
    H["Protected Endpoint"]
end

subgraph Tokens["🔑 Tokens"]
    I["Access Token\n30 minutes"]
    J["Refresh Token\n7 days"]
    K["New Access Token"]
end

subgraph Frontend["⚛️ Axios Interceptor"]
    L["Intercept 401"]
    M["Call /auth/refresh"]
    N["Update localStorage"]
    O["Retry Original Request"]
end

A --> F
F --> I
F --> J
B --> C
C --> H
H -->|"401"| D
D --> L
L --> G
G -->|"Valid"| K
K --> M
M --> N
N --> O
O --> H
H -->|"200 OK"| Client
```

---

# Refresh Token Sequence

```mermaid
sequenceDiagram

actor Client
participant App as React App
participant Axios as Axios Interceptor
participant AuthAPI as /api/v1/auth/refresh
participant ProtectedAPI as /api/v1/jobs
participant JWT as JWT Utility

Client->>App: Make API request
App->>Axios: GET /api/v1/jobs (with access_token)
Axios->>ProtectedAPI: GET /api/v1/jobs (Authorization: Bearer access_token)

alt Access Token Valid
    ProtectedAPI-->>Axios: 200 OK
    Axios-->>App: Data
    App-->>Client: Display jobs
else Access Token Expired (401)
    ProtectedAPI-->>Axios: 401 Unauthorized
    
    Axios->>Axios: Check refresh_token exists
    Note over Axios: Automatically retries once
    
    Axios->>AuthAPI: POST /auth/refresh {refresh_token}
    AuthAPI->>JWT: decode_token(refresh_token)
    
    alt Refresh Token Valid
        JWT-->>AuthAPI: Valid claims
        AuthAPI->>JWT: create_access_token(user_id)
        JWT-->>AuthAPI: new_access_token
        AuthAPI-->>Axios: {access_token: "new_jwt..."}
        Axios->>Axios: Update localStorage
        Axios->>ProtectedAPI: Retry original request with new token
        ProtectedAPI-->>Axios: 200 OK
        Axios-->>App: Data
        App-->>Client: Display jobs
    else Refresh Token Expired
        AuthAPI-->>Axios: 401
        Axios->>Axios: Clear localStorage
        Axios->>Axios: Redirect to /login
    end
end
```

---

# Token Specifications

| Token | Lifetime | Payload | Used For |
|-------|----------|---------|----------|
| Access Token | 30 minutes | `sub` (user_id), `email`, `role`, `type: "access"`, `iat`, `exp`, `jti` | API Authorization (Bearer header) |
| Refresh Token | 7 days | `sub` (user_id), `type: "refresh"`, `iat`, `exp`, `jti` | Generating new access tokens |

---

# Frontend Auto-Refresh (Axios Interceptor)

```
Request → 401 → Check refresh_token
                     ↓
              Has token? ──No──→ Redirect to /login
                     │
                    Yes
                     │
              POST /auth/refresh
                     │
               ┌─────┴─────┐
              Valid       Invalid
               │            │
          Store new       Clear tokens
          access_token    Redirect /login
               │
          Retry original
          request
```

---

# Security Rules

- Access Token cannot be used to generate a new Access Token
- Refresh Token must contain `type: "refresh"` claim
- Expired tokens are rejected with 401
- Invalid JWT signature is rejected
- Frontend auto-refresh only retries once per request
- If refresh fails, all tokens are cleared and user is redirected to login

---

# Token Flow Status

| Feature | Status |
|---------|:------:|
| Access Token generation | ✅ |
| Refresh Token generation | ✅ |
| Token refresh endpoint | ✅ |
| JWT signature verification | ✅ |
| Frontend auto-refresh interceptor | ✅ |
| Token expiry handling | ✅ |
| Logout (clear tokens) | ✅ |
| Refresh Token rotation | 🔜 Planned |
| Token revocation | 🔜 Planned |
