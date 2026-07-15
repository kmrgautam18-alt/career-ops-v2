# Deployment Diagram

Version: 1.0

Status: Active

---

# Purpose

This diagram describes the production deployment architecture for Career-Ops v2 using Docker Compose and AWS EC2.

---

# Production Architecture

```mermaid
flowchart TD

    Internet["🌐 Internet"]
    DNS["DNS
yourdomain.com"]
    EC2["☁️ AWS EC2 Instance
Ubuntu 24.04 LTS"]
    Nginx["🌐 Nginx (port 80)
Serves Frontend + API Proxy"]
    Frontend["⚛️ React + Vite
Static Build"]
    Backend["🚀 FastAPI Backend
uvicorn (port 8000)"]
    PostgreSQL[(🗄 PostgreSQL 16
port 5432)]
    Storage["💾 Docker Volume
postgres_data"]

    Internet --> DNS
    DNS --> EC2
    EC2 --> Nginx
    Nginx -->|"/" static| Frontend
    Nginx -->|"/api/*" proxy| Backend
    Backend --> PostgreSQL
    PostgreSQL --> Storage
```

---

# Docker Compose Stack

```yaml
services:
  postgres:
    image: postgres:16-alpine
    volume: postgres_data
    healthcheck: pg_isready

  backend:
    build: ./Dockerfile
    env: DATABASE_URL, SECRET_KEY, CORS_ORIGINS
    depends_on: postgres (healthy)

  frontend:
    build: ./frontend/Dockerfile
    nginx: serves built static files
    depends_on: backend
```

---

# Deployment Flow

```mermaid
sequenceDiagram

    actor Dev as Developer
    participant Git as GitHub
    participant CI as GitHub Actions
    participant EC2 as AWS EC2
    participant App as Docker Stack

    Dev->>Git: git push origin main
    Git->>CI: Trigger deploy workflow
    CI->>EC2: SSH into instance
    CI->>EC2: git pull
    CI->>EC2: docker compose up -d --build
    CI->>EC2: alembic upgrade head
    EC2->>App: Restart services
    App-->>Dev: https://yourdomain.com
```

---

# Server Specifications

| Resource | Value |
|----------|-------|
| Instance type | `t3.medium` (2 vCPU, 4 GB RAM) |
| Storage | 20 GB gp3 |
| OS | Ubuntu 24.04 LTS |
| Docker | Latest CE |
| Docker Compose | Latest |

---

# Security Group

| Port | Protocol | Source | Purpose |
|------|----------|--------|---------|
| 22 | TCP | Your IP | SSH |
| 80 | TCP | 0.0.0.0/0 | HTTP (frontend) |
| 443 | TCP | 0.0.0.0/0 | HTTPS (future) |

> ⚠️ Port 8000 (backend) is NOT exposed publicly — Nginx proxies API requests internally.

---

# Deployment Scripts

| Script | Purpose |
|--------|---------|
| `scripts/ec2-bootstrap.sh` | One-time: installs Docker, clones repo, sets up env |
| `scripts/deploy-ec2.sh` | Ongoing: rsyncs code, rebuilds stack, runs migrations |
| `scripts/setup-ec2-instance.md` | Step-by-step setup guide with IAM and security group |

---

# Environment Variables (Production)

| Variable | Source |
|----------|--------|
| `DATABASE_URL` | `postgresql://user:pass@postgres:5432/careerops` |
| `SECRET_KEY` | `openssl rand -hex 64` |
| `CORS_ORIGINS` | `https://yourdomain.com` |
| `POSTGRES_PASSWORD` | Strong random password |
| `APP_ENV` | `production` |
| `DEBUG` | `false` |

---

# Health Check

```bash
# Verify the deployment
curl https://yourdomain.com
# → {"application":"Career-Ops v2","status":"healthy"}

# API docs
curl https://yourdomain.com/docs
```
