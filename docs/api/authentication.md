# Authentication API

## Module

Authentication & Authorization

---

# Overview

The Authentication module provides secure user authentication using JWT (JSON Web Token).

Passwords are hashed using Argon2.

The authentication system is stateless and suitable for horizontal scaling.

---

# Features

* User Registration
* Secure Password Hashing (Argon2)
* JWT Access Token
* JWT Refresh Token
* Login Authentication
* Exception Handling
* Standard API Response
* Role Support

---

# Authentication Flow

```text
Client
    │
POST /api/v1/auth/login
    │
    ▼
FastAPI Router
    │
    ▼
Authentication Service
    │
    ▼
User Repository
    │
    ▼
SQLite Database
    │
Verify Password
    │
Argon2
    │
Generate JWT
    │
Return Tokens
```

---

# Login Endpoint

## URL

POST /api/v1/auth/login

---

## Request

```json
{
    "email":"kumar@example.com",
    "password":"StrongPassword123!"
}
```

---

## Success Response

HTTP 200

```json
{
    "success": true,
    "message": "Login successful.",
    "data": {
        "access_token": "<JWT_ACCESS_TOKEN>",
        "refresh_token": "<JWT_REFRESH_TOKEN>",
        "token_type": "bearer"
    }
}
```

---

## Invalid Credentials

HTTP 401

```json
{
    "success": false,
    "message": "Invalid email or password."
}
```

---

## Inactive User

HTTP 403

```json
{
    "success": false,
    "message": "User account is inactive."
}
```

---

# JWT Claims

## Access Token

* sub
* email
* role
* type
* iat
* exp
* jti

## Refresh Token

* sub
* type
* iat
* exp
* jti

---

# Security

* Argon2 Password Hashing
* HS256 JWT
* Stateless Authentication
* Refresh Token Support
* Custom Exception Handling

---

# Module Status

| Feature            | Status |
| ------------------ | ------ |
| Registration       | ✅      |
| Password Hashing   | ✅      |
| JWT                | ✅      |
| Login              | ✅      |
| Exception Handling | ✅      |

---

Current Version

Authentication Module v1.0
