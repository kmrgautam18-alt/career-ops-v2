# Security Policy

## Supported Versions

| Version | Supported |
|---------|:---------:|
| 0.1.x   | ✅ Active |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Career-Ops v2, please follow these steps:

1. **Do NOT** open a public GitHub issue
2. Email the maintainer directly (see GitHub profile)
3. Include a detailed description of the vulnerability
4. Include steps to reproduce (if possible)

### What to expect

- **Acknowledgment**: Within 48 hours
- **Update**: Within 1 week on status
- **Fix**: Timeline depends on severity

## Security Practices

- 🔐 **JWT Authentication** — Access tokens (30m) + Refresh tokens (7d)
- 🔑 **Argon2 Password Hashing** — Industry-standard password hashing
- 🛡️ **RBAC** — Role-based access control (USER / ADMIN)
- 📝 **Input Validation** — Pydantic schema validation on all endpoints
- 🐳 **Docker Isolation** — Services run in isolated containers
- 🔒 **Environment Variables** — All secrets via env vars, never in code

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | JWT signing secret (generate with `openssl rand -hex 64`) |
| `DATABASE_URL` | Database connection string |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `CORS_ORIGINS` | Allowed CORS origins |
