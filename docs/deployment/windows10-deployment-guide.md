# 🪟 Career-Ops Windows 10 Deployment Guide — Zero Cost, Live on Internet

> **Goal:** Deploy Career-Ops v2 on your **Windows 10** machine and make it live on the internet **without spending any money**.

**Difficulty:** 🟢 Beginner | **Time:** ~30 minutes | **Total Cost:** $0.00

---

## 📋 Overview — How Windows 10 Goes Live for Free

| Need | Free Solution | How To Get It |
|------|---------------|---------------|
| 🐳 **Docker** | Docker Desktop for Windows (free) | `docker.com` → Download → Install |
| 🐧 **Linux Environment** | WSL2 (Windows Subsystem for Linux) | Built into Windows 10 — enable in 2 clicks |
| 🌐 **Static Domain** | DuckDNS (`yourname.duckdns.org`) | `duckdns.org` — free, no credit card |
| 🔒 **HTTPS** | Cloudflare Tunnel (free TLS 1.3) | `dash.cloudflare.com` — free plan |
| 🤖 **AI Engine** | Google Gemini (free tier, 60 req/min) | `aistudio.google.com` — free API key |
| 📧 **Email** | Gmail App Password | Free Google account |
| 📱 **Notifications** | Telegram Bot | `@BotFather` on Telegram — free |
| 🔄 **Automation** | n8n (self-hosted in Docker) | Included in Career-Ops stack |
| 📊 **Monitoring** | Prometheus + Grafana (self-hosted) | Included in Career-Ops stack| **Total: $0.00 for everything**

---

## ⚡ Quick Deploy with WSL (Interactive — 2 Minutes)

If you're comfortable with the command line, the **interactive deploy script** automates the Linux-side setup (Docker, DuckDNS, Cloudflare, admin accounts, monitoring) after WSL2 is installed.

```bash
# Inside your WSL2 Ubuntu terminal:
bash scripts/deploy-rhel-interactive.sh

# Or download directly from GitHub (no clone needed):
curl -fsSL https://raw.githubusercontent.com/kmrgautam18-alt/career-ops-v2/main/scripts/deploy-rhel-interactive.sh | bash
```

> **⚠️ Important:** You still need to complete **Steps 1-2** of this guide first (enable WSL2 + install Docker Desktop with WSL2 integration). After that, run the interactive script inside WSL2 to finish setup.

### What the Script Does vs. Manual Steps

| Phase | Interactive Script | Manual Equivalent |
|-------|:------------------|:------------------|
| 🔧 System Setup | Installs Docker, git, curl, jq | Steps 1-2 (WSL2 + Docker) |
| 📦 Clone & .env | Clones repo, generates random secrets | Steps 3-5 |
| 🐳 Docker Stack | Builds & starts all services | Steps 6 |
| 🌐 DuckDNS | Sets up domain with auto-update | Steps 7 |
| ☁️ Cloudflare | Creates free HTTPS tunnel | Steps 8 |
| ✅ Verification | Health-checks everything | Steps 9 |
| 🤖 n8n Automation | Imports all 6 workflows | Steps 10 |

```bash
# Preview everything without making changes:
bash scripts/deploy-rhel-interactive.sh --dry-run
```

> **💡 Tip:** Run with `--dry-run` first to see the full plan inside WSL2. Then re-run without it to go live.

---

## 🛠️ What You Need Before Starting

### Required Software
| Software | Why | Download |
|----------|-----|----------|
| **Docker Desktop** | Runs Career-Ops containers | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) |
| **Git for Windows** | Clone the repository | [git-scm.com](https://git-scm.com) |
| **Windows Terminal** (recommended) | Better terminal experience | Microsoft Store — free |
| **Google Chrome** or **Edge** | Access the dashboard | Already installed |

### Free Accounts to Create
| Account | Sign Up At | What You Get |
|---------|-----------|--------------|
| **DuckDNS** | [duckdns.org](https://duckdns.org) | Free domain like `careerops.duckdns.org` |
| **Google AI Studio** | [aistudio.google.com](https://aistudio.google.com) | Free Gemini API key (60 req/min) |
| **Cloudflare** | [dash.cloudflare.com](https://dash.cloudflare.com) | Free HTTPS + Tunnel (optional) |
| **Telegram** | [telegram.org](https://telegram.org) | Messaging app + free bot notifications |

---

## 📑 Table of Contents

1. [Enable WSL2 (Windows Subsystem for Linux)](#-step-1-enable-wsl2)
2. [Install Docker Desktop](#-step-2-install-docker-desktop)
3. [Clone Career-Ops](#-step-3-clone-career-ops)
4. [Get Your Free Accounts](#-step-4-get-free-accounts)
5. [Configure Environment](#-step-5-configure-environment)
6. [Build & Start Docker Services](#-step-6-build--start-docker)
7. [Set Up Free Domain with DuckDNS](#-step-7-free-domain-with-duckdns)
8. [Set Up Free HTTPS with Cloudflare](#-step-8-free-https-with-cloudflare)
9. [Verify Everything Works](#-step-9-verify-everything)
10. [Set Up n8n Workflows](#-step-10-set-up-n8n-workflows)
11. [Post-Deployment Checklist](#-step-11-post-deployment-checklist)
12. [Daily Operations](#-step-12-daily-operations)
13. [Troubleshooting Windows 10 Issues](#-step-13-troubleshooting-windows-10)

---

## ✅ Step 1: Enable WSL2

WSL2 lets Docker run Linux containers natively on Windows. This is required for Docker Desktop.

### 1.1 Check Windows Version
1. Press `Windows + R`, type `winver`, press Enter
2. You need **Windows 10 build 19041+** (released May 2020)
3. If you have an older build, run **Windows Update** first

### 1.2 Enable WSL2 (2 methods)

**Method A: One Command (Easiest)**

Open **PowerShell as Administrator** (right-click Start → Windows PowerShell (Admin)):

```powershell
wsl --install
```

This installs WSL2 + Ubuntu automatically. **Restart your computer** when prompted.

**Method B: Manual (if Method A fails)**

```powershell
# Step 1: Enable WSL feature
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Step 2: Enable Virtual Machine Platform
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Step 3: Restart
Restart-Computer

# Step 4: Set WSL2 as default
wsl --set-default-version 2

# Step 5: Install Ubuntu from Microsoft Store
# Open Microsoft Store → Search "Ubuntu" → Install
```

### 1.3 Verify WSL2

```powershell
wsl --status
# Should show: Default Version: 2
```

---

## 🐳 Step 2: Install Docker Desktop

### 2.1 Download & Install
1. Go to [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Click **Download for Windows** (free)
3. Run the installer (`Docker Desktop Installer.exe`)
4. **IMPORTANT:** Check ✅ "Use WSL 2 instead of Hyper-V"
5. Click OK and let it install (takes 2-3 minutes)
6. **Restart your computer** when prompted

### 2.2 Configure Docker
1. After restart, Docker Desktop should start automatically
2. If not, search "Docker Desktop" in Start Menu and launch it
3. Wait for the whale icon in system tray to stop animating (turns steady)
4. Right-click the whale icon → **Settings** → **Resources** → **WSL Integration**
5. Ensure your Ubuntu distro is toggled ON
6. Click **Apply & Restart**

### 2.3 Verify Docker

Open **Windows Terminal** or **PowerShell**:

```powershell
docker --version
# Should show: Docker version 24.0.x or higher

docker compose version
# Should show: Docker Compose version v2.x.x

docker run hello-world
# Should show: "Hello from Docker!" message
```

---

## 📦 Step 3: Clone Career-Ops

### 3.1 Open PowerShell/Terminal

Press `Windows + X` → **Windows Terminal** (or PowerShell)

Navigate to where you want the project:

```powershell
# Create a projects folder on your C: drive
mkdir C:\Projects
cd C:\Projects
```

### 3.2 Clone the Repository

```powershell
git clone https://github.com/kmrgautam18-alt/career-ops-v2.git
cd career-ops-v2
```

### 3.3 Verify Clone

```powershell
dir
# You should see: backend/, frontend/, docker-compose.yml, scripts/, etc.
```

---

## 🔑 Step 4: Get Your Free Accounts

### 4.1 DuckDNS — Free Domain (2 minutes)

1. Open [duckdns.org](https://duckdns.org) in your browser
2. Click **Sign in with** (Google, GitHub, or Twitter) — pick whatever you have
3. Under "Domains", enter a name: `careerops`
4. Click **Add Domain**
5. Your domain is now: **`careerops.duckdns.org`**
6. **Copy your "token"** — it's a long string of letters/numbers. Save it!

### 4.2 Google Gemini AI — Free API Key (2 minutes)

1. Open [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API Key** → **Create API Key**
4. Select an existing project or create new
5. **Copy your API key** — starts with `AIza...`. Save it!

### 4.3 Cloudflare — Free HTTPS (5 minutes, optional but recommended)

1. Open [dash.cloudflare.com](https://dash.cloudflare.com)
2. Sign up for a free account
3. Go to **Zero Trust** → **Access** → **Tunnels**
4. Click **Create a tunnel** → Name it: `careerops-tunnel` → **Save**
5. Under "Connectors", choose **Docker**
6. Copy the **token** (starts with `eyJhI...`). Save it!
7. On the "Public Hostname" tab:
   - Subdomain: `careerops`
   - Domain: `duckdns.org`
   - Service: `http://localhost:80`
   - Save

### 4.4 Telegram Bot (2 minutes, optional)

1. Open Telegram on your phone or desktop
2. Search for **@BotFather**
3. Send: `/newbot`
4. Name: `CareerOps Notifier`
5. Username: `careerops_notifier_bot`
6. **Copy the token** (format: `1234567890:ABCdef...`). Save it!
7. Search for your bot `@careerops_notifier_bot` and click **Start**
8. Send any message like `/start`
9. Get your Chat ID:
   ```powershell
   # In PowerShell, replace YOUR_BOT_TOKEN:
   curl -s "https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates"
   # Look for "chat":{"id": 123456789}
   ```

### 4.5 Gmail App Password (2 minutes, optional for email)

1. Go to [myaccount.google.com](https://myaccount.google.com) → **Security**
2. Turn ON **2-Step Verification** (required for App Passwords)
3. Go to **Security** → **App Passwords** (search if not visible)
4. Select: App = **Mail**, Device = **Other** → Name: `Career-Ops`
5. **Copy the 16-character password** (format: `abcd efgh ijkl mnop`). Save it!

---

## ⚙️ Step 5: Configure Environment

### 5.1 Create the .env File

In PowerShell, inside `C:\Projects\career-ops-v2`:

```powershell
# Copy the example env file
copy .env.example .env

# Open in Notepad
notepad .env
```

### 5.2 Edit the .env File

Replace the values with what you saved in Step 4:

```env
# ── Database (auto-generate) ──────────────
POSTGRES_DB=careerops
POSTGRES_USER=careerops
POSTGRES_PASSWORD=YourSuperSecurePassword123!

# ── JWT (use a random password) ───────────
SECRET_KEY=YourSuperSecretKeyChangeMe1234567890!

# ── AI / Gemini (from Step 4.2) ───────────
LLM_API_KEY=AIzaSy...your-actual-gemini-key...

# ── Grafana ───────────────────────────────
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=YourGrafanaPassword123

# ── n8n ───────────────────────────────────
N8N_ENCRYPTION_KEY=YourRandomEncryptionKey12345678

# ── CORS ──────────────────────────────────
CORS_ORIGINS=http://localhost:3000,https://careerops.duckdns.org

# ── SMTP (from Step 4.5, optional) ────────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM_EMAIL=your.email@gmail.com
SMTP_ENABLED=false
```

### 5.3 Create Required Directories

```powershell
mkdir data
mkdir monitoring\loki
mkdir backups\postgres
```

---

## 🐳 Step 6: Build & Start Docker

### 6.1 Start the Stack

```powershell
# Make sure Docker Desktop is running
# In PowerShell, inside C:\Projects\career-ops-v2:

docker compose up -d --build
```

**What this does:** Downloads images and builds Career-Ops. **First time takes 5-10 minutes** depending on your internet.

### 6.2 Watch the Build Progress

You'll see output like:
```
[+] Building 125.3s (25/25) FINISHED
[+] Running 13/13
 ✔ Container careerops-db              Started
 ✔ Container careerops-redis           Started
 ✔ Container careerops-backend         Started
 ✔ Container careerops-frontend        Started
 ✔ Container careerops-prometheus      Started
 ✔ Container careerops-grafana         Started
 ✔ Container careerops-alertmanager    Started
 ✔ Container careerops-loki            Started
 ✔ Container careerops-promtail        Started
 ✔ Container careerops-n8n             Started
 ✔ Container careerops-celery-worker   Started
 ✔ Container careerops-celery-beat     Started
 ✔ Container careerops-n8n             Started
```

### 6.3 Verify All Running

```powershell
docker compose ps
```

All services should show **"Up"** status.

### 6.4 Run Database Migrations

```powershell
docker compose exec backend alembic upgrade head
```

---

## 🌐 Step 7: Free Domain with DuckDNS

### 7.1 Set Up DuckDNS Updater on Windows

On Windows 10, we'll use a scheduled task to keep your IP updated.

**Method A: PowerShell Script (Recommended)**

Create the updater script:

```powershell
# Create the scripts directory
mkdir C:\Projects\career-ops-v2\scripts\windows 2>$null

# Create the update script
@"
# DuckDNS Update Script for Windows
# Replace YOUR_TOKEN and careerops with your actual values
`$token = "YOUR_DUCK_DNS_TOKEN"
`$domain = "careerops"
`$url = "https://www.duckdns.org/update?domains=$domain&token=$token&ip="

try {
    `$response = Invoke-WebRequest -Uri `$url -UseBasicParsing
    `$content = `$response.Content
    Write-Output "$(Get-Date): $content" | Out-File -FilePath "C:\Projects\career-ops-v2\scripts\windows\duck.log" -Append
    Write-Host "DuckDNS updated: $content"
} catch {
    Write-Output "$(Get-Date): Failed: $_" | Out-File -FilePath "C:\Projects\career-ops-v2\scripts\windows\duck.log" -Append
    Write-Host "Failed: $_"
}
"@ | Out-File -FilePath "C:\Projects\career-ops-v2\scripts\windows\update-duckdns.ps1" -Encoding utf8
```

**Now edit the script with YOUR actual token:**

```powershell
notepad C:\Projects\career-ops-v2\scripts\windows\update-duckdns.ps1
```

Replace `YOUR_DUCK_DNS_TOKEN` with the token from DuckDNS (Step 4.1).

### 7.2 Test the Script

```powershell
powershell -ExecutionPolicy Bypass -File C:\Projects\career-ops-v2\scripts\windows\update-duckdns.ps1
```

Expected output: `DuckDNS updated: OK`

### 7.3 Schedule Automatic Updates (Every 5 Minutes)

1. Press `Windows + R`, type `taskschd.msc`, press Enter
2. Click **Create Task** on the right panel
3. **General tab:**
   - Name: `CareerOps DuckDNS Updater`
   - Check: ✅ "Run whether user is logged on or not"
   - Check: ✅ "Run with highest privileges"
4. **Triggers tab:**
   - Click **New** → Begin the task: **On a schedule**
   - **Daily**, Starting now, **Repeat every 5 minutes** for **Indefinitely**
   - Click OK
5. **Actions tab:**
   - Click **New** → Action: **Start a program**
   - Program: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "C:\Projects\career-ops-v2\scripts\windows\update-duckdns.ps1"`
   - Click OK
6. **Conditions tab:**
   - Uncheck: ❌ "Stop if the computer switches to battery power"
   - Click OK
7. Click **OK** to save

Your DuckDNS domain will now stay updated automatically! 🎉

### 7.4 Test Your Domain

```powershell
ping careerops.duckdns.org
# Should resolve to your public IP

# Also test via browser
start https://careerops.duckdns.org
```

---

## ☁️ Step 8: Free HTTPS with Cloudflare Tunnel

### 8.1 Install cloudflared on Windows

1. Download cloudflared from:
   [developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
2. Download the **Windows 64-bit** version
3. Move `cloudflared.exe` to `C:\Projects\career-ops-v2\scripts\windows\`

### 8.2 Create the Tunnel Script

```powershell
# Create a batch file to start Cloudflare Tunnel
@"
@echo off
REM Career-Ops Cloudflare Tunnel
REM Start this script when you want HTTPS access
cd /d "C:\Projects\career-ops-v2\scripts\windows"
cloudflared.exe tunnel --no-autoupdate run --token YOUR_CLOUDFLARE_TUNNEL_TOKEN
"@ | Out-File -FilePath "C:\Projects\career-ops-v2\scripts\windows\start-tunnel.bat" -Encoding ascii
```

**Edit the file to add your tunnel token:**

```powershell
notepad C:\Projects\career-ops-v2\scripts\windows\start-tunnel.bat
```

Replace `YOUR_CLOUDFLARE_TUNNEL_TOKEN` with the token from Step 4.3.

### 8.3 Start the Tunnel

**Option A: Manual Start** — Double-click `start-tunnel.bat` whenever you want HTTPS access.

**Option B: Automatic Start with Docker**

```powershell
docker run -d --restart=always --name cloudflared `
  cloudflare/cloudflared:latest tunnel --no-autoupdate run --token YOUR_CLOUDFLARE_TUNNEL_TOKEN
```

### 8.4 Configure Cloudflare Dashboard

1. Go to [dash.cloudflare.com](https://dash.cloudflare.com)
2. Zero Trust → Access → Tunnels → Click your tunnel
3. **Public Hostname** tab → **Add a public hostname**
4. Subdomain: `careerops`
5. Domain: `duckdns.org`
6. Service: `http://localhost:80`
7. Additional settings:
   - TLS: **Full (strict)**
   - Always Use HTTPS: **ON**
   - Auto Minify: **ON**

### 8.5 Verify HTTPS

```powershell
# Wait 2 minutes for Cloudflare to provision
curl -sI https://careerops.duckdns.org
# Should return: HTTP/1.1 200 OK
```

**Your app is now live at `https://careerops.duckdns.org` with HTTPS! 🔒**

---

## ✅ Step 9: Verify Everything

### 9.1 Health Checks in PowerShell

```powershell
# 1. Check all Docker services
docker compose ps

# 2. Backend health
curl http://localhost:8000/health
# Expected: {"status":"healthy","checks":{"database":{"status":"healthy"},"llm":{"status":"healthy"}}}

# 3. Backend readiness (for Kubernetes)
curl http://localhost:8000/ready
# Expected: {"status":"ready"}

# 4. Backend liveness
curl http://localhost:8000/live
# Expected: {"status":"alive"}

# 5. Prometheus metrics
curl http://localhost:8000/metrics
# Expected: lots of metrics starting with "careerops_"

# 6. Check n8n
curl http://localhost:5678/healthz
# Expected: {"status":"ok"}
```

### 9.2 Create Your First User

```powershell
# Register a new user
curl -X POST http://localhost:8000/api/v1/users/register `
  -H "Content-Type: application/json" `
  -d '{"email":"admin@example.com","password":"YourPass123!","username":"admin","full_name":"Career-Ops Admin"}'

# Login to get JWT token
$TOKEN = curl -s -X POST http://localhost:8000/api/v1/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email":"admin@example.com","password":"YourPass123!"}' | `
  python -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])"

Write-Host "Token: $TOKEN"
```

### 9.3 Test AI Features

```powershell
# Test ATS scoring
curl -X POST http://localhost:8000/api/v1/ai/ats-score `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $TOKEN" `
  -d '{"resume_text":"Python developer with 5 years Docker and AWS experience","job_description":"Senior backend Python engineer needed"}'

# If you see "overall_score" — AI is working! 🎉
```

---

## 🤖 Step 10: Set Up n8n Workflows

### 10.1 Access n8n

1. Open your browser: `http://localhost:5678`
2. Create an admin account (any email/password — this is local)
3. You'll see the n8n dashboard

### 10.2 Import All 6 Workflows

```powershell
# First, make sure the workflows folder is accessible
dir C:\Projects\career-ops-v2\monitoring\n8n\workflows\
```

**In n8n (your browser):**
1. Click **Workflows** in the left sidebar
2. Click **Import from File** (top right)
3. Select each file and import ALL 6:

| # | File | What It Does |
|:-:|------|-------------|
| 1 | `job-alert-workflow.json` | Scrapes jobs every 6 hours, notifies you |
| 2 | `application-status-email.json` | Sends email when application status changes |
| 3 | `daily-digest-workflow.json` | Daily 8 AM summary of your career stats |
| 4 | `follow-up-automation-workflow.json` | Auto follow-up emails for pending apps |
| 5 | `interview-detection-workflow.json` | Notifies when interviews are scheduled |
| 6 | `telegram-notifications.json` | All events → Telegram instantly |

### 10.3 Configure Credentials in n8n

In n8n, go to **Credentials** → **New** → Create the following:

| Credential Type | What For | Your Values |
|----------------|----------|-------------|
| **Telegram** | Telegram notifications | Bot token from Step 4.4 |
| **SMTP** | Email notifications | Gmail settings from Step 4.5 |
| **HTTP Header Auth** | Career-Ops API | Your JWT token from Step 9.2 |
| **Slack** (optional) | Slack notifications | Webhook URL from Slack |

### 10.4 Enable Webhooks

In n8n, open each webhook-triggered workflow and copy its webhook URL.
Then in your `.env` file:

```env
N8N_ENABLED=true
N8N_WEBHOOK_BASE_URL=http://n8n:5678
```

Restart the backend:
```powershell
docker compose restart backend
```

### 10.5 Activate All Workflows

In n8n, for each workflow:
1. Click **Save** (or Ctrl+S)
2. Toggle the **Active** switch (top right) to ON
3. Verify: Workflow shows "Active" badge

---

## ✅ Step 11: Post-Deployment Checklist

| # | Task | Status | How to Verify |
|:-:|------|:------:|--------------|
| 1 | WSL2 installed and default | ☐ | `wsl --status` shows version 2 |
| 2 | Docker Desktop running | ☐ | Whale icon steady in system tray |
| 3 | All 13+ Docker services up | ☐ | `docker compose ps` — all "Up" |
| 4 | DuckDNS domain configured | ☐ | `ping careerops.duckdns.org` resolves |
| 5 | DuckDNS auto-updater running | ☐ | Task Scheduler shows the task |
| 6 | Cloudflare Tunnel active | ☐ | `https://careerops.duckdns.org` loads |
| 7 | Gemini API key set | ☐ | `/health` shows `llm.status: healthy` |
| 8 | Admin user created | ☐ | Can login at `http://localhost:5173` |
| 9 | n8n accessible | ☐ | `http://localhost:5678` loads |
| 10 | All 6 n8n workflows imported | ☐ | n8n shows 6 workflows |
| 11 | n8n workflows activated | ☐ | All show "Active" badge |
| 12 | Webhooks enabled | ☐ | `N8N_ENABLED=true` in `.env` |
| 13 | Grafana accessible | ☐ | `http://localhost:3001` loads |
| 14 | LinkedIn auto-poster set up | ☐ | `scripts/linkedin-automation.sh` works |

---

## 🔄 Step 12: Daily Operations

### Start Career-Ops

```powershell
# Make sure Docker Desktop is running
# Then in PowerShell:
cd C:\Projects\career-ops-v2
docker compose up -d

# Start Cloudflare Tunnel (for HTTPS)
docker start cloudflared 2>$null | Out-Null
```

### Stop Career-Ops

```powershell
docker compose down
docker stop cloudflared 2>$null | Out-Null
```

### View Logs

```powershell
# All services
docker compose logs --tail=50

# Specific service
docker compose logs --tail=50 backend
docker compose logs --tail=50 n8n
```

### Generate LinkedIn Post

```powershell
bash scripts/linkedin-automation.sh --daily
```

### Backup Database

```powershell
bash scripts/backup-db.sh
```

### Update Career-Ops

```powershell
cd C:\Projects\career-ops-v2
git pull origin main
docker compose up -d --build
```

---

## ❓ Step 13: Troubleshooting Windows 10 Issues

### ❌ Docker Desktop won't start

```
Problem: Docker Desktop crashes on launch
Fix:    Enable virtualization in BIOS
        1. Restart PC → Press F2/DEL to enter BIOS
        2. Find "Intel VT-x" or "AMD-V" → Enable
        3. Save and exit
        4. Also enable in Windows: 
           PowerShell (Admin):
           dism.exe /online /enable-feature /featurename:Microsoft-Hyper-V /all /norestart
```

### ❌ WSL2 not installing

```
Problem: wsl --install fails
Fix:    Manual installation:
        PowerShell (Admin):
        dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all
        dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all
        Restart → Install Ubuntu from Microsoft Store
```

### ❌ Port 80 already in use

```
Problem: "port is already allocated"
Fix:    Something else is using port 80 (IIS, Skype, etc.)
        
        # Find what's using port 80:
        netstat -ano | findstr :80
        
        # Stop IIS (if installed):
        Stop-Service W3SVC
        Set-Service W3SVC -StartupType Disabled
        
        # Or change Career-Ops to use a different port:
        # In docker-compose.yml, change frontend ports to "8080:80"
```

### ❌ Docker containers keep restarting

```
Problem: Containers show "Restarting"
Fix:    Check logs:
        docker compose logs --tail=50 backend
        
        # Most common cause: PostgreSQL not ready
        # Fix: restart the stack:
        docker compose restart postgres
        sleep 10
        docker compose restart backend
```

### ❌ DuckDNS not updating

```
Problem: Domain doesn't resolve to your IP
Fix:    Your public IP changed. Run the updater manually:
        PowerShell:
        C:\Projects\career-ops-v2\scripts\windows\update-duckdns.ps1
        
        Then check Task Scheduler:
        - Is the task enabled?
        - Is it running every 5 minutes?
        - Check C:\Projects\career-ops-v2\scripts\windows\duck.log for errors
```

### ❌ Can't access from phone/tablet

```
Problem: Works on PC but not on other devices
Fix:    Windows Firewall is blocking connections
        1. Open "Windows Defender Firewall" 
        2. Advanced Settings → Inbound Rules
        3. New Rule → Port → TCP → 80, 443, 8000, 5678
        4. Allow the connection
        5. Name: "Career-Ops Inbound"
```

### ❌ AI features returning errors

```
Problem: "LLM is not configured"
Fix:    Set your Gemini API key:
        1. Open C:\Projects\career-ops-v2\.env
        2. Verify: LLM_API_KEY=AIza...your-key
        3. Restart: docker compose restart backend
```

### ❌ Performance is slow

```
Problem: Windows feels sluggish with Docker running
Fix:    WSL2 memory limits:
        1. Create/edit: %USERPROFILE%\.wslconfig
        2. Add:
           [wsl2]
           memory=4GB
           processors=2
        3. Restart WSL: wsl --shutdown
```

---

## 📊 Service Map (Windows 10)

```
┌─────────────────────────────────────────────────────────────────┐
│                    🌐 Your Windows 10 PC                         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Docker Desktop (WSL2 Backend)                │   │
│  │                                                           │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────────┐   │   │
│  │  │ Frontend│ │ Backend│ │Postgres│ │  Redis Cache   │   │   │
│  │  │ :80     │ │ :8000  │ │ :5432  │ │  :6379         │   │   │
│  │  └────────┘ └───┬────┘ └────────┘ └────────────────┘   │   │
│  │                  │                                       │   │
│  │  ┌───────────────▼─────────────────────────────────┐   │   │
│  │  │           Celery Workers + Beat                  │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────────┐   │   │
│  │  │Prometheus│ │ Grafana │ │ n8n    │ │  Cloudflared  │   │   │
│  │  │ :9090   │ │ :3001   │ │ :5678  │ │  (HTTPS)       │   │   │
│  │  └────────┘ └────────┘ └────────┘ └────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
│                            ▼                                    │
│              ┌────────────────────────┐                        │
│              │ ☁️ Cloudflare Tunnel    │                        │
│              │  → careerops.duckdns.org│                        │
│              │  → HTTPS (TLS 1.3)      │                        │
│              │  → DDoS Protection      │                        │
│              └────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 What You Get for $0 on Windows 10

| Feature | Cost |
|---------|:----:|
| ✅ Docker Desktop + WSL2 | **$0** |
| ✅ Career-Ops platform (16 services) | **$0** |
| ✅ Free domain: `careerops.duckdns.org` | **$0** |
| ✅ HTTPS / SSL via Cloudflare | **$0** |
| ✅ Google Gemini AI (60 req/min) | **$0** |
| ✅ n8n workflow automation (6 workflows) | **$0** |
| ✅ Telegram notifications | **$0** |
| ✅ Email via Gmail App Password | **$0** |
| ✅ Prometheus + Grafana monitoring | **$0** |
| ✅ LinkedIn auto-poster | **$0** |
| ✅ Redis caching (10x faster) | **$0** |

**Total: $0.00/month**

---

<div align="center">

## 🎉 Career-Ops is LIVE on Windows 10!

**Open:** `https://careerops.duckdns.org`

**If Cloudflare isn't set up yet:** `http://localhost:5173`

### Quick Links

| Service | URL |
|---------|-----|
| Career-Ops App | `http://localhost:5173` |
| API Docs | `http://localhost:8000/docs` |
| n8n Automation | `http://localhost:5678` |
| Grafana | `http://localhost:3001` |
| Prometheus | `http://localhost:9090` |

### Commands to Remember

```powershell
# Start everything
docker compose up -d

# Stop everything
docker compose down

# View logs
docker compose logs --tail=50 backend

# Generate LinkedIn post
bash scripts/linkedin-automation.sh --daily

# Check health
curl http://localhost:8000/health
```

---

**🚀 Your Career, Supercharged by AI — All from Windows 10, All for Free!**

</div>
