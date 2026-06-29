# Authentication Flow Diagram

## Overview

This document describes the authentication workflow implemented in Career-Ops v2.

Authentication uses:

* Argon2 Password Hashing
* JWT Access Token
* JWT Refresh Token
* Stateless Authentication
* Custom Exception Handling

---

# Authentication Sequence

```mermaid
                           Authentication Flow

+--------------------+
|      Client        |
+--------------------+
          |
          | POST /api/v1/auth/login
          v
+--------------------+
|  FastAPI Router    |
|    auth.py         |
+--------------------+
          |
          v
+--------------------+
|   Auth Service     |
| login_user()       |
+--------------------+
          |
          v
+----------------------------+
| User Repository            |
| get_user_by_email()        |
+----------------------------+
          |
          v
+----------------------------+
| SQLite Database            |
+----------------------------+
          |
          v
User Found?
     |
 +---+------------------+
 |                      |
 | No                   | Yes
 |                      |
 v                      v
401 Unauthorized   Verify Password
                        |
                        v
                +------------------+
                | Argon2 Verify    |
                +------------------+
                        |
            +-----------+-----------+
            |                       |
            | Invalid               | Valid
            |                       |
            v                       v
    401 Unauthorized       User Active?
                                    |
                        +-----------+-----------+
                        |                       |
                        | No                    | Yes
                        |                       |
                        v                       v
                 403 Forbidden         Generate JWT
                                              |
                                              v
                              +---------------------------+
                              | JWT Utility               |
                              |                           |
                              | Access Token              |
                              | Refresh Token             |
                              +---------------------------+
                                              |
                                              v
                              HTTP 200 OK Response
```

---

# Components

## API Layer

* auth.py

## Service Layer

* auth_service.py

## Repository Layer

* user_repository_sa.py

## Security Layer

* password.py
* jwt.py

## Database

* SQLite

---

# Exceptions

| Exception                   | HTTP Status |
| --------------------------- | ----------: |
| InvalidCredentialsException |         401 |
| InactiveUserException       |         403 |
| UserNotFoundException       |         404 |
| DuplicateEmailException     |         409 |
| DuplicateUsernameException  |         409 |
| UnauthorizedException       |         401 |

---

# Status

Authentication Module v1

* User Registration ✅
* Login ✅
* Password Hashing ✅
* JWT Authentication ✅
* Exception Handling ✅
