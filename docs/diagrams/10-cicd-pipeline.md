# CI/CD Pipeline

Version: 1.0

Status: Active

---

# Purpose

This diagram illustrates the CI/CD pipeline for Career-Ops v2 — from code push to production deployment.

---

# CI/CD Pipeline Overview

```mermaid
flowchart LR

    Dev["👨‍💻 Developer\nCode Changes"]
    Git["🐙 GitHub\nRepository"]
    CI["🔨 GitHub Actions\nCI Pipeline"]
    Tests["🧪 Automated Tests\nBackend: 98 tests\nFrontend: Typecheck"]
    Build["📦 Build\nDocker Images"]
    Deploy["🚀 Deploy\nEC2 / RHEL VM"]
    Prod["🌐 Production\nCareer-Ops Stack"]
    Monitor["📊 Monitoring\nHealth Checks\nLogs"]

    Dev -->|"git push"| Git
    Git -->|"Trigger"| CI
    CI -->|"Run"| Tests
    Tests -->|"Pass"| Build
    Build -->|"Push"| Deploy
    Deploy -->|"docker compose up"| Prod
    Prod -->|"Observe"| Monitor
    Monitor -->|"Feedback"| Dev
```

---

# GitHub Actions Workflow

```mermaid
sequenceDiagram

    actor Dev as Developer
    participant GH as GitHub
    participant CI as GitHub Actions
    participant Backend as Backend Tests
    participant Frontend as Frontend Checks
    participant EC2 as EC2 Server

    Dev->>GH: git push origin main
    GH->>CI: Trigger workflow

    par CI Pipeline
        CI->>Backend: Run pytest (98 tests)
        Backend-->>CI: ✅ All tests passed

        CI->>Frontend: bun tsc --noEmit
        Frontend-->>CI: ✅ Typecheck passed

        CI->>Frontend: bun run build
        Frontend-->>CI: ✅ Build successful
    end

    CI->>CI: All checks passed
    CI->>EC2: SSH + deploy

    EC2->>EC2: git pull
    EC2->>EC2: docker compose up -d --build
    EC2->>EC2: docker compose exec backend alembic upgrade head

    EC2-->>CI: ✅ Deployment complete
    CI-->>Dev: ✅ Success notification
```

---

# Pipeline Stages

| Stage | Tool | Duration | Description |
|-------|------|----------|-------------|
| 1. Trigger | GitHub | Instant | Push to `main` branch |
| 2. Backend Tests | pytest | ~12s | 98 tests (auth, jobs, apps, resume, AI, extraction) |
| 3. Frontend Typecheck | `tsc -b` | ~5s | TypeScript 6 strict mode |
| 4. Frontend Build | Vite | ~3s | Production build → `dist/` |
| 5. Deploy | `deploy-ec2.sh` | ~30s | RSync code → Docker Compose → Migrations |

---

# Deployment Targets

```mermaid
flowchart TD

    Repo["🐙 GitHub\nkmrgautam18-alt/career-ops-v2"]

    subgraph Local["💻 Local Development"]
        BackendDev["Backend\nuvicorn :8000"]
        FrontendDev["Frontend\nbun dev :5173"]
    end

    subgraph Docker["🐳 Docker Compose"]
        DB["PostgreSQL 16"]
        API["FastAPI Backend"]
        UI["Nginx + Frontend"]
    end

    subgraph EC2["☁️ AWS EC2 / RHEL VM"]
        DockerCompose["Docker Compose Stack"]
    end

    Repo -->|"git pull"| Local
    Repo -->|"deploy script"| Docker
    Repo -->|"deploy-ec2.sh"| EC2
    Docker -->|"docker compose up"| Local
    EC2 --> DockerCompose
```

---

# Current CI Status

| Check | Status |
|-------|:------:|
| Backend tests (98) | ✅ Passing |
| Frontend typecheck | ✅ 0 errors |
| Frontend production build | ✅ Successful |
| Docker Compose build | ✅ Verified |
| Deploy scripts | ✅ Ready (EC2 + RHEL) |
| Automated GitHub Actions | 🔜 Planned |

---

# Deploy Scripts

| Script | Target | Command |
|--------|--------|---------|
| `scripts/deploy-ec2.sh` | AWS EC2 | `EC2_HOST=... bash scripts/deploy-ec2.sh` |
| `scripts/deploy-rhel.sh` | RHEL 10.2 VM | `sudo bash scripts/deploy-rhel.sh` |
| `scripts/preview.sh` | Local dev | `bash scripts/preview.sh` |

---

# Deployment Commands

```bash
# Full stack with Docker
docker compose up -d --build

# Run migrations
docker compose exec backend alembic upgrade head

# View logs
docker compose logs -f backend

# Update and redeploy
git pull && docker compose up -d --build
```
