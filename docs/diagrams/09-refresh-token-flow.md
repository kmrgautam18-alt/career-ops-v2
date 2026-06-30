# Refresh Token Flow

## Overview

The Refresh Token module allows clients to obtain a new Access Token without requiring the user to log in again.

The Refresh Token is long-lived and can only be used to generate a new Access Token.

---

# Authentication Lifecycle

```mermaid
flowchart LR

subgraph Client["👤 Client"]
    A["Login"]
end

subgraph Auth["🔐 Authentication"]
    B["Generate Access Token"]
    C["Generate Refresh Token"]
end

subgraph Runtime["⚙️ Runtime"]
    D["Protected APIs"]
    E["Access Token Expired"]
end

subgraph Refresh["🔄 Refresh Flow"]
    F["POST /api/v1/auth/refresh"]
    G["Validate Refresh Token"]
    H["Generate New Access Token"]
end

subgraph Response["📦 Response"]
    I["HTTP 200"]
    J["HTTP 401"]
end

A --> B
A --> C

B --> D

D --> E

E --> F

F --> G

G -->|Valid| H

H --> I

G -->|Invalid| J
```

---

# Refresh Token Sequence

```mermaid
sequenceDiagram

actor Client

participant API as Auth API
participant JWT as JWT Utility

Client->>API: POST /auth/refresh

API->>JWT: Decode Refresh Token

alt Invalid Token

JWT-->>API: Unauthorized

API-->>Client: HTTP 401

else Valid Refresh Token

JWT-->>API: Claims

API->>JWT: Generate New Access Token

JWT-->>API: JWT

API-->>Client: HTTP 200

end
```

---

# Token Lifecycle

| Token | Lifetime | Purpose |
|--------|----------|----------|
| Access Token | 30 Minutes | Access Protected APIs |
| Refresh Token | 7 Days | Generate New Access Token |

---

# Security Rules

- Access Token cannot refresh itself.
- Refresh Token must contain `type = refresh`.
- Expired Refresh Token is rejected.
- Invalid signature is rejected.
- JWT signature is always verified.
- Refresh endpoint never returns a new Refresh Token (v1).

---

# Future Enhancements

- Refresh Token Rotation
- Token Revocation
- Redis Session Store
- Multi-device Sessions
- Logout Everywhere
- Device Fingerprinting

---

# Sprint Status

| Feature | Status |
|---------|:------:|
| Login | ✅ |
| JWT | ✅ |
| RBAC | ✅ |
| Refresh Token | 🔄 |
| Logout | ⏳ |
| Token Rotation | ⏳ |

---

**Sprint:** Sprint 9.3 — Refresh Token Flow