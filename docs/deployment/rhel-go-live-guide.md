# 🌐 Career-Ops RHEL Go-Live Guide — Zero-Cost Production Deployment

> **Goal:** Deploy Career-Ops v2 on your RHEL 10.2 VM and make it live on the internet **without spending any money**.

**Last Updated:** 2026-07-16 | **Total Cost:** $0.00/month

---

## 🧠 Overview — How We Go Live for Free

| Need | Free Solution | Why It Works |
|------|---------------|-------------|
| 🖥️ **VM / Server** | Your existing RHEL 10.2 machine | Already have it! |
| 🌐 **Static IP** | Cloudflare Tunnel (no public IP needed) | Works behind NAT, no static IP required |
| 🔗 **Domain** | `duckdns.org` (free subdomain) | `yourname.duckdns.org` — fully customizable |
| 🔒 **HTTPS / SSL** | Cloudflare (auto SSL + DDoS protection) | Free TLS 1.3, automatic renewal |
| 🗄️ **PostgreSQL** | Docker container on your VM | Included in Docker Compose |
| 🤖 **AI Engine** | Google Gemini (free tier: 60 req/min) | No credit card required for Gemini API |
| 🐳 **Docker / Podman** | Free, open-source | `dnf install podman` (RHEL default) or `dnf install docker-ce` |
| 📊 **Monitoring** | Prometheus + Grafana (self-hosted) | Included in the stack |
| 🔔 **Alerting** | Alertmanager (Slack webhook — free) | Slack's free tier is enough |
| 🤖 **Automation** | n8n (self-hosted) | Included in Docker Compose |
| ☁️ **DNS** | Cloudflare DNS (free plan) | Fast, DDoS protected |

**Total infrastructure cost: $0/month.**

---

## 📋 Prerequisites

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|:-------:|:-----------:|
| CPU | 2 cores | 4 cores |
| RAM | 4 GB | 8 GB |
| Disk | 20 GB free | 50 GB SSD |
| OS | RHEL 10.2 / Fedora 40+ | RHEL 10.2 |
| Network | Outbound internet | Stable connection |

### What You Need to Sign Up For (All Free)

1. **Cloudflare account** → [cloudflare.com](https://cloudflare.com) (free plan)
2. **DuckDNS account** → [duckdns.org](https://duckdns.org) (free)
3. **Slack workspace** → [slack.com](https://slack.com) (free — optional for alerts)
4. **Google AI Studio** → [aistudio.google.com](https://aistudio.google.com) → Get Gemini API key (free)

---

## ⚡ Quick Deploy (Interactive — 2 Minutes)

> Skip the manual steps! The **interactive deploy script** automates everything from Docker to DuckDNS, Cloudflare, admin accounts, and monitoring — all with smart defaults. Press Enter to accept any prompt.

```bash
# One command on your RHEL VM:
bash scripts/deploy-rhel-interactive.sh

# Or download directly from GitHub (no clone needed):
curl -fsSL https://raw.githubusercontent.com/kmrgautam18-alt/career-ops-v2/main/scripts/deploy-rhel-interactive.sh | bash
```

### What the Script Does vs. Manual Steps

| Phase | Interactive Script | Manual Equivalents |
|-------|:------------------|:-------------------|
| 🔧 System Setup | Auto-detects Podman (RHEL default) or Docker, installs engine + compose + git, curl, jq, cron | Phase 1 |
| 📦 Clone & .env | Clones repo, generates random secrets | Phase 2 |
| 🌐 DuckDNS | Sets up `yourdomain.duckdns.org` + cron | Phase 3 |
| ☁️ Cloudflare HTTPS | Creates free TLS tunnel | Phase 4 |
| 🔥 Firewall | Opens required ports | Phase 5 |
| 🐳 Container Stack | Builds & starts all 16 containers via detected engine | Phase 6 |
| 👤 Admin User | Runs migrations, creates admin | Phase 7 |
| 🔄 Automation | Daily backups + LinkedIn + n8n workflows | Phase 7 |
| ✅ Verification | Health-checks all services | Phase 7 |
| 🎉 Summary | Saves all credentials to file | — |

```bash
# Preview everything without making changes:
bash scripts/deploy-rhel-interactive.sh --dry-run
```

> **💡 Tip:** Run with `--dry-run` first to see the full plan. Then re-run without it to go live.

---

## 🚀 Manual Step-by-Step Deployment (Zero Cost)

> Use this guide if you prefer full control, or want to understand every step the interactive script automates.

### Phase 1: System Preparation (5 minutes)

> **💡 The interactive script auto-detects your engine.** RHEL ships Podman by default — the script installs it automatically. Use Docker CE only if you have a specific need for it.

**Podman (RHEL native — recommended):**
```bash
sudo dnf install -y podman podman-docker podman-compose
```

**Docker CE (alternative):**
```bash
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

### Phase 2: Clone & Configure (3 minutes)

```bash
# 4. Clone the repository
cd ~
git clone https://github.com/kmrgautam18-alt/career-ops-v2.git
cd career-ops-v2

# 5. Create the .env file (no secrets to buy!)
cat > .env << 'EOF'
# ── Database ──────────────────────────────
POSTGRES_DB=careerops
POSTGRES_USER=careerops
POSTGRES_PASSWORD=$(openssl rand -hex 32)

# ── JWT Security ──────────────────────────
SECRET_KEY=$(openssl rand -hex 32)

# ── AI / Gemini ───────────────────────────
LLM_API_KEY=your-gemini-api-key-here

# ── Grafana ───────────────────────────────
GRAFANA_ADMIN_PASSWORD=$(openssl rand -hex 16)

# ── n8n ───────────────────────────────────
N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)

# ── CORS ──────────────────────────────────
CORS_ORIGINS=http://localhost:3000,https://yourname.duckdns.org

# ── SMTP (Gmail App Password — free) ──────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM_EMAIL=your.email@gmail.com
SMTP_ENABLED=false

# ── Redis / Celery ────────────────────────
REDIS_ENABLED=true
CELERY_ENABLED=false

# ── OAuth (Optional) ─────────────────────
OAUTH_ENABLED=false
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
EOF

# 6. Generate the actual secrets
sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$(openssl rand -hex 32)/" .env
sed -i "s/SECRET_KEY=.*/SECRET_KEY=$(openssl rand -hex 32)/" .env
sed -i "s/GRAFANA_ADMIN_PASSWORD=.*/GRAFANA_ADMIN_PASSWORD=$(openssl rand -hex 16)/" .env
sed -i "s/N8N_ENCRYPTION_KEY=.*/N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)/" .env

echo "✅ .env configured with random secrets"
```

### Phase 3: Free Domain with DuckDNS (5 minutes)

```bash
# 7. Register your free domain
# Go to https://duckdns.org
# Sign in with Google/GitHub/Twitter
# Create a subdomain: "careerops" → careerops.duckdns.org
# → Your public IP will auto-update

# 8. Install DuckDNS updater (keeps IP updated)
sudo mkdir -p /opt/duckdns
sudo tee /opt/duckdns/duck.sh << 'DUCKEOF'
#!/bin/bash
# Replace YOUR_TOKEN with the token from duckdns.org
echo url="https://www.duckdns.org/update?domains=careerops&token=YOUR_DUCK_DNS_TOKEN&ip=" | curl -k -o /opt/duckdns/duck.log -s -
DUCKEOF
sudo chmod +x /opt/duckdns/duck.sh

# Test it
sudo /opt/duckdns/duck.sh
cat /opt/duckdns/duck.log
# Expected: OK

# 9. Set up cron to update every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * sudo /opt/duckdns/duck.sh >/dev/null 2>&1") | crontab -
```

### Phase 4: Free HTTPS with Cloudflare Tunnel (10 minutes)

```bash
# 10. Set up Cloudflare Tunnel (no public IP needed!)
# Step A: Go to https://dash.cloudflare.com → Zero Trust → Access → Tunnels
# Step B: Create a tunnel → "careerops-tunnel" → Save
# Step C: Copy the tunnel token (starts with eyJhI...)

# 11. Connect with Docker (as root)
sudo docker run -d --restart=always --name cloudflared \
  cloudflare/cloudflared:latest tunnel --no-autoupdate run --token YOUR_TUNNEL_TOKEN

# 12. Configure tunnel in Cloudflare Dashboard
# Public hostname: careerops.duckdns.org
# Service: http://localhost:80
# Additional settings:
#   - TLS: Full (strict)
#   - Always Use HTTPS: ON
#   - Auto Minify: ON

echo "✅ Cloudflare Tunnel configured — HTTPS active automatically"
```

### Phase 5: Firewall Setup (2 minutes)

```bash
# 13. Configure firewall — only allow Cloudflare IPs
# Cloudflare publishes their IP ranges at https://www.cloudflare.com/ips-v4

# Remove default port 80/443 rules (Cloudflare tunnel handles ingress)
sudo firewall-cmd --permanent --remove-service=http 2>/dev/null || true
sudo firewall-cmd --permanent --remove-service=https 2>/dev/null || true

# Allow Docker services
sudo firewall-cmd --permanent --add-port=8000/tcp    # Backend API
sudo firewall-cmd --permanent --add-port=5678/tcp    # n8n (admin only)

# Only allow monitoring from localhost
sudo firewall-cmd --permanent --add-port=9090/tcp    # Prometheus
sudo firewall-cmd --permanent --add-port=3001/tcp    # Grafana
sudo firewall-cmd --permanent --add-port=9093/tcp    # Alertmanager

# Reload
sudo firewall-cmd --reload
```

### Phase 6: Deploy (3 minutes)

```bash
# 14. Set your Gemini API key (GET FREE: https://aistudio.google.com)
# In the .env file above, replace "your-gemini-api-key-here" with your actual key
nano .env
# Update LLM_API_KEY=your-actual-key

# 15. Create directories
mkdir -p data monitoring/loki monitoring/n8n/workflows backups/postgres

# 16. Build and start the full stack
docker compose up -d --build

# 17. Run database migrations
docker compose exec backend alembic upgrade head || true

# 18. Verify all services are up
docker compose ps
```

### Phase 7: Verify (2 minutes)

```bash
# Quick health checks
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/live

# Verify AI is working (set up first user)
curl -X POST http://localhost:8000/api/v1/users/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@example.com","password":"YourPass123!","username":"admin","full_name":"Admin"}'

# Verify the app is accessible through Cloudflare
curl https://careerops.duckdns.org
```

---

## 🏁 Post-Deployment Checklist

| Step | Task | Status |
|:----:|------|:------:|
| 1 | DuckDNS subdomain created (`careerops.duckdns.org`) | ☐ |
| 2 | DuckDNS token updated in `/opt/duckdns/duck.sh` | ☐ |
| 3 | Cloudflare Tunnel token set up | ☐ |
| 4 | Gemini API key added to `.env` | ☐ |
| 5 | Docker services all running (`docker compose ps`) | ☐ |
| 6 | First user registered via API | ☐ |
| 7 | App loads at `https://careerops.duckdns.org` | ☐ |
| 8 | Login and create data | ☐ |
| 9 | Grafana at `http://your-vm-ip:3001` (admin / password in .env) | ☐ |
| 10 | 🔐 (Optional) Set Grafana password-based auth only | ☐ |

---

## 🔄 Daily Operations

### Check System Health

```bash
# Quick health summary
curl https://careerops.duckdns.org/health

# Docker status
docker compose ps

# Disk usage
df -h /

# Docker logs (last 50 lines)
docker compose logs --tail=50 backend
```

### Backup Your Database (Automated)

```bash
# Manual backup
bash scripts/backup-db.sh

# Set up automatic daily backups at 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * cd ~/career-ops-v2 && bash scripts/backup-db.sh --cron") | crontab -
```

### Update Your Deployment

```bash
cd ~/career-ops-v2
git pull origin main
docker compose up -d --build --remove-orphans
docker compose exec backend alembic upgrade head
```

### Monitor for Free

| Tool | URL | Purpose |
|------|-----|---------|
| 📊 **Grafana** | `http://vm-ip:3001` (admin:password) | Full dashboard + logs |
| 📈 **Prometheus** | `http://vm-ip:9090` | Raw metrics explorer |
| 🔔 **Alertmanager** | `http://vm-ip:9093` | Active alerts |
| 🚦 **DuckDNS** | `https://duckdns.org` | Domain status |
| ☁️ **Cloudflare** | `https://dash.cloudflare.com` | Tunnel health, analytics |

### Connect Slack Alerts (Free)

```bash
# 1. Go to your Slack workspace
# 2. Create a channel: #careerops-alerts
# 3. Add "Incoming Webhooks" app
# 4. Copy webhook URL: https://hooks.slack.com/services/T.../B.../xxx

# 5. Update Alertmanager config
nano monitoring/alertmanager/alertmanager.yml
# Uncomment and add your webhook URL:
# slack_api_url: 'https://hooks.slack.com/services/T.../B.../xxx'

# 6. Restart
docker compose up -d alertmanager
```

---

## 🧠 Adding Free AI (Gemini)

```bash
# 1. Go to https://aistudio.google.com
# 2. Click "Get API Key" → Create API Key
# 3. Copy the key
# 4. Add it to .env:
echo 'LLM_API_KEY="your-gemini-key-here"' >> .env
# 5. Restart backend:
docker compose restart backend
```

**Gemini Free Tier Limits:**
- 60 requests per minute
- 1,000 requests per day
- Models: `gemini-2.0-flash` (included)

**This is more than enough for personal use!**

---

## 🆘 Troubleshooting — No-Cost Solutions

| Problem | Solution |
|---------|----------|
| ❌ **DuckDNS not resolving** | Check cron: `crontab -l` — IP changed? Run updater manually |
| ❌ **Cloudflare Tunnel failing** | Check: `docker logs cloudflared --tail=20` |
| ❌ **AI features not working** | Set `LLM_API_KEY` in `.env` — get free key from [aistudio.google.com](https://aistudio.google.com) |
| ❌ **Port 80 already in use** | Stop Apache/nginx: `sudo systemctl stop httpd` |
| ❌ **Docker permission denied** | Run: `sudo usermod -aG docker $USER && newgrp docker` |
| ❌ **SMTP not sending** | Gmail: Enable 2FA → Generate App Password (free) — or set `SMTP_ENABLED=false` |
| ❌ **Out of disk space** | Run: `docker system prune -af` (removes unused images, frees GBs) |
| ❌ **n8n workflows visible** | Create admin account at: `http://vm-ip:5678` on first visit |

---

## 📊 Full Service Map (16 Docker Services)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ☁️ Cloudflare Tunnel                             │
│                   (Free TLS + DDoS Protection)                       │
│                              │                                       │
│                    careerops.duckdns.org                             │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Docker Compose Stack                       │   │
│  │                                                               │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐   │   │
│  │  │  🌐 Nginx   │  │ 🚀 Backend │  │  🗃️ PostgreSQL       │   │   │
│  │  │  :80 (SPA)  │──│  :8000 API │──│  :5432                │   │   │
│  │  │  :443 (SSL) │  │  /metrics  │  └──────────────────────┘   │   │
│  │  └────────────┘  └─────┬──────┘                               │   │
│  │                        │                                       │   │
│  │  ┌────────────┐  ┌─────▼──────┐  ┌──────────────────────┐   │   │
│  │  │  🔴 Redis   │  │ ⚙️ Celery  │  │  🤖 Gemini AI        │   │   │
│  │  │  :6379      │  │ Worker+Beat│  │  (external API)       │   │   │
│  │  └────────────┘  └────────────┘  └──────────────────────┘   │   │
│  │                                                               │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐   │   │
│  │  │  📊 Prom.   │  │ 📈 Grafana │  │  🔔 Alertmanager      │   │   │
│  │  │  :9090      │──│  :3001     │  │  :9093                │   │   │
│  │  └────┬───────┘  └────────────┘  └──────────────────────┘   │   │
│  │       │                                                       │   │
│  │  ┌────▼───────┐  ┌────────────┐  ┌──────────────────────┐   │   │
│  │  │  📝 Loki    │  │ 🔍 Promtail│  │  🤖 n8n               │   │   │
│  │  │  :3100      │  │ (log agent)│  │  :5678                │   │   │
│  │  └────────────┘  └────────────┘  └──────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🌟 What You Get for $0

| Feature | Cost |
|---------|:----:|
| ✅ Production-quality career management platform | **$0** |
| ✅ AI-powered ATS scoring, interview prep, resume optimization | **$0** |
| ✅ Auto-apply engine (scrape, tailor, send, follow-up) | **$0** |
| ✅ Full monitoring: Prometheus + Grafana + Alertmanager | **$0** |
| ✅ Centralized logging: Loki + Promtail | **$0** |
| ✅ Workflow automation: n8n (5 pre-built workflows) | **$0** |
| ✅ Custom domain: `yourname.duckdns.org` | **$0** |
| ✅ HTTPS / SSL (TLS 1.3) via Cloudflare | **$0** |
| ✅ DDoS protection via Cloudflare | **$0** |
| ✅ Google Gemini AI (60 req/min free tier) | **$0** |
| ✅ Redis caching for 10x faster responses | **$0** |
| ✅ Celery background workers for async AI | **$0** |
| ✅ Slack alerts (free tier) | **$0** |
| ✅ SMTP email via Gmail App Password | **$0** |
| ✅ Automatic backups | **$0** |
| ✅ CI/CD pipeline (GitHub Actions free tier) | **$0** |

**Total monthly cost: $0.00**

Your Career-Ops deployment is now live at **`https://careerops.duckdns.org`** 🚀
