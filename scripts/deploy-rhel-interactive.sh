#!/bin/bash
# =============================================================================
# Career-Ops v2 — Interactive RHEL Deployment
# =============================================================================
# Single script to deploy Career-Ops on a fresh RHEL VM.
# 
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/kmrgautam18-alt/career-ops-v2/main/scripts/deploy-rhel-interactive.sh | bash
#   # OR locally:
#   bash scripts/deploy-rhel-interactive.sh
#
# What it does:
#   ✓ Installs Docker + system dependencies
#   ✓ Clones Career-Ops repository
#   ✓ Prompts for config (press Enter to auto-default)
#   ✓ Sets up DuckDNS free domain
#   ✓ Configures Cloudflare Tunnel (optional)
#   ✓ Builds & starts all 16 Docker services
#   ✓ Creates admin user
#   ✓ Sets up daily backups + LinkedIn automation
#   ✓ Verifies everything is working
#
# Requirements:
#   - Fresh RHEL 9/10 VM with internet access
#   - DuckDNS token (free: https://duckdns.org)
#   - Gemini API key (free: https://aistudio.google.com)
# =============================================================================

set -euo pipefail

# ── Color Codes ─────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# ── Config ──────────────────────────────────────────────────────────────
REPO_URL="https://github.com/kmrgautam18-alt/career-ops-v2.git"
PROJECT_DIR="$HOME/career-ops-v2"
DEPLOY_LOG="/tmp/careerops-deploy-$(date +%Y%m%d_%H%M%S).log"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# ── Logger ──────────────────────────────────────────────────────────────
exec 3>&1 4>&2
exec >> "$DEPLOY_LOG" 2>&1

log()    { echo -e "${GREEN}[✓]${NC} $*" | tee /dev/fd/3; }
warn()   { echo -e "${YELLOW}[!]${NC} $*" | tee /dev/fd/3; }
error()  { echo -e "${RED}[✗]${NC} $*" | tee /dev/fd/3; }
header() {
    echo "" | tee /dev/fd/3
    echo -e "${MAGENTA}════════════════════════════════════════════════${NC}" | tee /dev/fd/3
    echo -e "${BOLD}  $*${NC}" | tee /dev/fd/3
    echo -e "${MAGENTA}════════════════════════════════════════════════${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
}
info()   { echo -e "${CYAN}  →${NC} $*" | tee /dev/fd/3; }

# ── Spinner ─────────────────────────────────────────────────────────────
spinner() {
    local pid=$1 msg=$2
    local spin='⣾⣽⣻⢿⡿⣟⣯⣷'
    local i=0
    while kill -0 "$pid" 2>/dev/null; do
        echo -ne "\r${YELLOW}${spin:$i:1}${NC} $msg" | tee /dev/fd/3
        i=$(( (i+1) % 8 ))
        sleep 0.1
    done
    echo -ne "\r${GREEN}✅${NC} $msg\n" | tee /dev/fd/3
}

# ── Prompt with Auto-Default ────────────────────────────────────────────
ask() {
    local var_name="$1" prompt_msg="$2" default_val="$3" is_secret="${4:-false}"
    local hint="${5:-}"
    
    if [ "$is_secret" = "true" ]; then
        echo -e "${CYAN}📝${NC} $prompt_msg" | tee /dev/fd/3
        [ -n "$hint" ] && echo -e "${DIM}     $hint${NC}" | tee /dev/fd/3
        echo -e "${DIM}     [default: $default_val]${NC}" | tee /dev/fd/3
        read -r -s -p "  ➤ " input
        echo ""
    else
        echo -e "${CYAN}📝${NC} $prompt_msg" | tee /dev/fd/3
        [ -n "$hint" ] && echo -e "${DIM}     $hint${NC}" | tee /dev/fd/3
        echo -e "${DIM}     [default: $default_val]${NC}" | tee /dev/fd/3
        read -r -p "  ➤ " input
    fi
    
    if [ -z "$input" ]; then
        eval "$var_name=\"$default_val\""
    else
        eval "$var_name=\"$input\""
    fi
}

# ── Confirm ─────────────────────────────────────────────────────────────
confirm() {
    local msg="$1"
    local default="${2:-y}"
    local prompt_str
    
    if [ "$default" = "y" ]; then
        prompt_str="[Y/n]"
    else
        prompt_str="[y/N]"
    fi
    
    echo -e "${CYAN}📝${NC} $msg $prompt_str" | tee /dev/fd/3
    read -r -p "  ➤ " input
    input=${input:-$default}
    
    if [[ "$input" =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# ── Banner ──────────────────────────────────────────────────────────────
print_banner() {
    clear 2>/dev/null || true
    echo -e "${CYAN}"
    echo '  ╔════════════════════════════════════════════════════════╗' | tee /dev/fd/3
    echo '  ║                                                        ║' | tee /dev/fd/3
    echo '  ║     🚀 Career-Ops v2 — Interactive Deployment          ║' | tee /dev/fd/3
    echo '  ║     Fresh RHEL VM → Live Internet in ~15 Minutes      ║' | tee /dev/fd/3
    echo '  ║                                                        ║' | tee /dev/fd/3
    echo '  ╚════════════════════════════════════════════════════════╝' | tee /dev/fd/3
    echo -e "${NC}" | tee /dev/fd/3
    echo -e "${DIM}  Log: $DEPLOY_LOG${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    echo -e "${YELLOW}  🔑 You need 2 FREE things to go live:${NC}" | tee /dev/fd/3
    echo -e "  ${CYAN}  1. DuckDNS token${NC} ${DIM}(https://duckdns.org — free domain)${NC}" | tee /dev/fd/3
    echo -e "  ${CYAN}  2. Gemini API key${NC} ${DIM}(https://aistudio.google.com — free AI)${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    echo -e "  ${DIM}  Everything else will auto-default if you press Enter.${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    if ! confirm "Ready to start deployment?"; then
        echo -e "${YELLOW}Deployment cancelled.${NC}" | tee /dev/fd/3
        exit 0
    fi
}

# ── Phase 1: Gather Configuration ──────────────────────────────────────
gather_config() {
    header "📋 Configuration"
    echo -e "${DIM}  Press Enter to accept defaults. Secrets stay local.${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    # ── DuckDNS ────────────────────────────────────────────────────────
    echo -e "${BOLD}  1. DuckDNS (Free Domain)${NC}" | tee /dev/fd/3
    echo -e "${DIM}     Go to https://duckdns.org → sign in → create a domain${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    ask DUCKDNS_DOMAIN "Enter your DuckDNS domain name" "careerops" false "e.g., 'careerops' → careerops.duckdns.org"
    ask DUCKDNS_TOKEN "Enter DuckDNS token" "" true "From duckdns.org → copy the token string"
    
    if [ -z "$DUCKDNS_TOKEN" ]; then
        warn "No DuckDNS token — skipping domain setup. You'll access via IP only."
        DUCKDNS_SKIP=true
    else
        DUCKDNS_SKIP=false
    fi
    echo "" | tee /dev/fd/3
    
    # ── Gemini AI ──────────────────────────────────────────────────────
    echo -e "${BOLD}  2. Google Gemini AI (Free)${NC}" | tee /dev/fd/3
    echo -e "${DIM}     Go to https://aistudio.google.com → Get API Key → Create${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    ask GEMINI_KEY "Enter Gemini API key" "" true "No credit card needed — free tier (60 req/min)"
    
    if [ -z "$GEMINI_KEY" ]; then
        warn "No Gemini key — AI features disabled. You can add later in .env"
    fi
    echo "" | tee /dev/fd/3
    
    # ── Cloudflare Tunnel (Optional) ───────────────────────────────────
    echo -e "${BOLD}  3. Cloudflare Tunnel (Free HTTPS — Recommended)${NC}" | tee /dev/fd/3
    echo -e "${DIM}     Go to https://dash.cloudflare.com → Zero Trust → Tunnels → Create${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    ask CF_TOKEN "Cloudflare tunnel token (or press Enter to skip)" "" true "Creates https://yourdomain.duckdns.org with HTTPS"
    
    if [ -z "$CF_TOKEN" ]; then
        warn "No Cloudflare token — will use http:// (not secure for internet)"
        echo -e "${YELLOW}     You can add HTTPS later via Cloudflare Tunnel.${NC}" | tee /dev/fd/3
    fi
    echo "" | tee /dev/fd/3
    
    # ── Telegram Bot (Optional) ────────────────────────────────────────
    echo -e "${BOLD}  4. Telegram Notifications (Optional)${NC}" | tee /dev/fd/3
    echo -e "${DIM}     Create a bot via @BotFather on Telegram → copy token${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    ask TELEGRAM_BOT_TOKEN "Telegram bot token (or press Enter to skip)" "" true "From @BotFather: format 123456:ABCdef"
    ask TELEGRAM_CHAT_ID "Telegram chat ID (or press Enter to skip)" "" false "Your user chat ID — send /start to bot, check getUpdates"
    echo "" | tee /dev/fd/3
    
    # ── SMTP / Email (Optional) ────────────────────────────────────────
    echo -e "${BOLD}  5. SMTP Email (Optional — for application emails)${NC}" | tee /dev/fd/3
    echo -e "${DIM}     Use Gmail App Password: Google Account → Security → App Passwords${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    ask SMTP_EMAIL "Gmail address (or press Enter to skip)" "" false "your.email@gmail.com"
    if [ -n "$SMTP_EMAIL" ]; then
        ask SMTP_PASSWORD "Gmail App Password" "" true "16-char password from Google App Passwords"
    fi
    echo "" | tee /dev/fd/3
    
    # ── Admin Account ──────────────────────────────────────────────────
    echo -e "${BOLD}  6. Admin Account${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    ask ADMIN_EMAIL "Admin email" "admin@careerops.com" false "Used to log in to the dashboard"
    ask ADMIN_PASS "Admin password" "Admin@12345" true "Min 8 characters"
    echo "" | tee /dev/fd/3
    
    # ── OAuth Social Login (Optional) ──────────────────────────────────
    echo -e "${BOLD}  7. OAuth Social Login (Optional)${NC}" | tee /dev/fd/3
    echo -e "${DIM}     Set up Google/GitHub login — requires OAuth client IDs${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    if confirm "Configure Google OAuth login?" "n"; then
        ask GOOGLE_CLIENT_ID "Google OAuth Client ID" "" false "From Google Cloud Console → Credentials"
        ask GOOGLE_CLIENT_SECRET "Google OAuth Client Secret" "" true ""
    else
        GOOGLE_CLIENT_ID=""
        GOOGLE_CLIENT_SECRET=""
    fi
    
    if confirm "Configure GitHub OAuth login?" "n"; then
        ask GITHUB_CLIENT_ID "GitHub OAuth Client ID" "" false "From GitHub → Settings → Developer Settings"
        ask GITHUB_CLIENT_SECRET "GitHub OAuth Client Secret" "" true ""
    else
        GITHUB_CLIENT_ID=""
        GITHUB_CLIENT_SECRET=""
    fi
    echo "" | tee /dev/fd/3
    
    # ── Summary ────────────────────────────────────────────────────────
    echo -e "${GREEN}─────────────────────────────────────────${NC}" | tee /dev/fd/3
    echo -e "  ${BOLD}Configuration Summary${NC}" | tee /dev/fd/3
    echo -e "${GREEN}─────────────────────────────────────────${NC}" | tee /dev/fd/3
    echo -e "  Domain:     ${CYAN}${DUCKDNS_SKIP:-false}${NC}" | tee /dev/fd/3
    [ "$DUCKDNS_SKIP" = false ] && echo -e "  Domain:     ${CYAN}https://${DUCKDNS_DOMAIN}.duckdns.org${NC}" | tee /dev/fd/3
    echo -e "  Admin:      ${CYAN}${ADMIN_EMAIL}${NC}" | tee /dev/fd/3
    echo -e "  AI:         ${CYAN}$([ -n \"$GEMINI_KEY\" ] && echo 'Gemini (free tier)' || echo 'Disabled')${NC}" | tee /dev/fd/3
    echo -e "  HTTPS:      ${CYAN}$([ -n \"$CF_TOKEN\" ] && echo 'Cloudflare Tunnel' || echo 'None (HTTP only)')${NC}" | tee /dev/fd/3
    echo -e "  Telegram:   ${CYAN}$([ -n \"$TELEGRAM_BOT_TOKEN\" ] && echo 'Configured' || echo 'None')${NC}" | tee /dev/fd/3
    echo -e "  Email:      ${CYAN}$([ -n \"$SMTP_EMAIL\" ] && echo \"${SMTP_EMAIL}\" || echo 'None')${NC}" | tee /dev/fd/3
    echo -e "  OAuth:      ${CYAN}$([ -n \"$GOOGLE_CLIENT_ID\" ] && echo 'Google + ')$([ -n \"$GITHUB_CLIENT_ID\" ] && echo 'GitHub')$([ -z \"$GOOGLE_CLIENT_ID\" ] && [ -z \"$GITHUB_CLIENT_ID\" ] && echo 'None')${NC}" | tee /dev/fd/3
    echo -e "${GREEN}─────────────────────────────────────────${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    if ! confirm "Deploy with these settings?"; then
        echo -e "${YELLOW}Deployment cancelled.${NC}" | tee /dev/fd/3
        exit 0
    fi
}

# ── Phase 2: System Setup ──────────────────────────────────────────────
phase_system() {
    header "🔥 System Preparation"
    
    log "Updating system packages..."
    sudo dnf update -y >> "$DEPLOY_LOG" 2>&1 &
    spinner $! "Updating packages"
    
    log "Installing Docker..."
    sudo dnf install -y dnf-plugins-core >> "$DEPLOY_LOG" 2>&1
    sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo >> "$DEPLOY_LOG" 2>&1 || true
    sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin >> "$DEPLOY_LOG" 2>&1 &
    spinner $! "Installing Docker"
    
    sudo systemctl enable --now docker >> "$DEPLOY_LOG" 2>&1
    sudo usermod -aG docker "$USER" >> "$DEPLOY_LOG" 2>&1
    
    log "Installing git, curl, jq, openssl..."
    sudo dnf install -y git curl jq openssl cronie nano >> "$DEPLOY_LOG" 2>&1 &
    spinner $! "Installing tools"
    
    # Firewall
    log "Opening firewall ports..."
    sudo firewall-cmd --permanent --add-port={80,443,8000,5678,3001,9090}/tcp 2>/dev/null || true
    sudo firewall-cmd --reload 2>/dev/null || true
    
    # SELinux
    if command -v getenforce &>/dev/null && [ "$(getenforce)" = "Enforcing" ]; then
        warn "SELinux is Enforcing — setting required booleans"
        sudo setsebool -P httpd_can_network_connect on 2>/dev/null || true
    fi
}

# ── Phase 3: Clone & Configure ─────────────────────────────────────────
phase_clone() {
    header "📦 Clone & Configure"
    
    cd "$HOME"
    
    log "Cloning Career-Ops..."
    if [ -d "$PROJECT_DIR" ]; then
        warn "Directory exists — pulling latest"
        cd "$PROJECT_DIR" && git pull origin main >> "$DEPLOY_LOG" 2>&1
    else
        git clone "$REPO_URL" >> "$DEPLOY_LOG" 2>&1 &
        spinner $! "Cloning repository"
    fi
    
    cd "$PROJECT_DIR"
    
    log "Generating secure .env..."
    POSTGRES_PASS=$(openssl rand -hex 32)
    SECRET_KEY=$(openssl rand -hex 32)
    GRAFANA_PASS=$(openssl rand -hex 16)
    N8N_KEY=$(openssl rand -hex 32)
    
    cat > .env << ENVEOF
# ── General ──────────────────────────────
APP_NAME=Career-Ops
APP_ENV=production
DEBUG=false

# ── Database ──────────────────────────────
DATABASE_URL=postgresql://careerops:${POSTGRES_PASS}@postgres:5432/careerops
POSTGRES_DB=careerops
POSTGRES_USER=careerops
POSTGRES_PASSWORD=${POSTGRES_PASS}

# ── JWT ───────────────────────────────────
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ── AI / Gemini ───────────────────────────
LLM_API_KEY=${GEMINI_KEY}
LLM_PROVIDER=google
LLM_MODEL=gemini-2.0-flash

# ── Grafana ───────────────────────────────
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=${GRAFANA_PASS}

# ── n8n ───────────────────────────────────
N8N_ENCRYPTION_KEY=${N8N_KEY}

# ── CORS ──────────────────────────────────
CORS_ORIGINS=http://localhost:3000,https://${DUCKDNS_DOMAIN}.duckdns.org
CORS_ALLOW_CREDENTIALS=true

# ── SMTP (Email) ──────────────────────────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=${SMTP_EMAIL}
SMTP_PASSWORD=${SMTP_PASSWORD}
SMTP_FROM_EMAIL=${SMTP_EMAIL}
SMTP_FROM_NAME=Career-Ops
SMTP_TLS=true
SMTP_ENABLED=$([ -n "${SMTP_EMAIL}" ] && echo "true" || echo "false")

# ── Redis / Celery ────────────────────────
REDIS_ENABLED=true
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
CELERY_ENABLED=true
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# ── OAuth (Social Login) ──────────────────
OAUTH_ENABLED=$([ -n "${GOOGLE_CLIENT_ID}" ] || [ -n "${GITHUB_CLIENT_ID}" ] && echo "true" || echo "false")
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
GITHUB_CLIENT_ID=${GITHUB_CLIENT_ID}
GITHUB_CLIENT_SECRET=${GITHUB_CLIENT_SECRET}

# ── Rate Limiting ─────────────────────────
RATE_LIMIT_ENABLED=true
RATE_LIMIT_DEFAULT=60
RATE_LIMIT_AI=10
RATE_LIMIT_AUTH=20

# ── Feature Flags ──────────────────────────
FEATURE_FLAGS_PATH=/data/feature_flags.json

# ── Baserow ───────────────────────────────
BASEROW_URL=
BASEROW_TOKEN=

# ── Telegram ──────────────────────────────
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
ENVEOF
    
    chmod 600 .env
    log ".env created with secure random secrets"
    
    mkdir -p data monitoring/loki backups/postgres
    log "Data directories created"
}

# ── Phase 4: DuckDNS ───────────────────────────────────────────────────
phase_duckdns() {
    if [ "$DUCKDNS_SKIP" = true ]; then
        log "Skipping DuckDNS (no token provided)"
        return
    fi
    
    header "🌐 DuckDNS — Free Domain"
    
    log "Setting up DuckDNS auto-updater..."
    sudo mkdir -p /opt/duckdns
    
    sudo tee /opt/duckdns/duck.sh > /dev/null << DUCKDNS
#!/bin/bash
TOKEN="${DUCKDNS_TOKEN}"
DOMAIN="${DUCKDNS_DOMAIN}"
LOG_FILE="/opt/duckdns/duck.log"
response=\$(curl -s "https://www.duckdns.org/update?domains=\${DOMAIN}&token=\${TOKEN}&ip=")
echo "\$(date): \$response" >> "\$LOG_FILE"
DUCKDNS
    
    sudo chmod +x /opt/duckdns/duck.sh
    
    log "Testing DuckDNS..."
    sudo /opt/duckdns/duck.sh >> "$DEPLOY_LOG" 2>&1
    if grep -q "OK" /opt/duckdns/duck.log 2>/dev/null; then
        log "✅ DuckDNS update successful!"
    else
        warn "DuckDNS test: $(cat /opt/duckdns/duck.log 2>/dev/null || echo 'failed')"
    fi
    
    log "Installing cron (every 5 minutes)..."
    (sudo crontab -l 2>/dev/null; echo "*/5 * * * * sudo /opt/duckdns/duck.sh >/dev/null 2>&1") | sudo crontab -
    log "Cron installed"
}

# ── Phase 5: Cloudflare Tunnel ─────────────────────────────────────────
phase_cloudflare() {
    if [ -z "${CF_TOKEN:-}" ]; then
        log "Skipping Cloudflare Tunnel"
        return
    fi
    
    header "☁️ Cloudflare Tunnel — Free HTTPS"
    
    log "Starting Cloudflare Tunnel container..."
    sudo docker run -d --restart=always --name cloudflared \
        cloudflare/cloudflared:latest tunnel --no-autoupdate run --token "$CF_TOKEN" >> "$DEPLOY_LOG" 2>&1
    
    log "✅ Cloudflare Tunnel started"
    info "Configure in Cloudflare Dashboard:"
    info "  Public hostname → ${DUCKDNS_DOMAIN}.duckdns.org"
    info "  Service → http://localhost:80"
    echo "" | tee /dev/fd/3
}

# ── Phase 6: Telegram Bot Setup ────────────────────────────────────────
phase_telegram() {
    if [ -z "${TELEGRAM_BOT_TOKEN:-}" ] || [ -z "${TELEGRAM_CHAT_ID:-}" ]; then
        log "Skipping Telegram notifications"
        return
    fi
    
    header "📱 Telegram — Notifications"
    
    # Test bot
    local test_result
    test_result=$(curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=🚀 Career-Ops deployment started!" 2>/dev/null)
    
    if echo "$test_result" | grep -q '"ok":true'; then
        log "✅ Telegram bot working!"
    else
        warn "Telegram test failed — check token and chat ID"
    fi
}

# ── Phase 7: Build & Start Docker ──────────────────────────────────────
phase_deploy() {
    header "🐳 Building & Starting Docker Stack"
    
    sudo systemctl start docker 2>/dev/null || true
    
    log "Building 16 Docker services (first time: 3-5 minutes)..."
    
    cd "$PROJECT_DIR"
    sudo docker compose up -d --build >> "$DEPLOY_LOG" 2>&1 &
    local build_pid=$!
    
    # Progress indicator
    local elapsed=0
    while kill -0 "$build_pid" 2>/dev/null; do
        if [ $((elapsed % 30)) -eq 0 ] && [ $elapsed -gt 0 ]; then
            echo -ne "\r${YELLOW}⏳${NC} Building... ${elapsed}s elapsed (tail -f $DEPLOY_LOG for details)\n" | tee /dev/fd/3
        fi
        sleep 2
        elapsed=$((elapsed + 2))
    done
    wait "$build_pid"
    
    echo -e "\r${GREEN}✅${NC} All services built and started!" | tee /dev/fd/3
    
    log "Waiting for services to be healthy..."
    sleep 10
    
    sudo docker compose ps --format "table {{.Name}}\t{{.Status}}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
}

# ── Phase 8: Initialize DB & User ──────────────────────────────────────
phase_init() {
    header "⚡ Database & User Setup"
    
    log "Running migrations..."
    sudo docker compose exec -T backend alembic upgrade head >> "$DEPLOY_LOG" 2>&1 || \
        warn "Migrations skipped"
    
    log "Creating admin user..."
    local login_check
    login_check=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"${ADMIN_EMAIL}\",\"password\":\"${ADMIN_PASS}\"}" 2>/dev/null || echo "failed")
    
    if echo "$login_check" | grep -q "access_token"; then
        log "✅ Admin user already exists"
    else
        local reg_response
        reg_response=$(curl -s -X POST http://localhost:8000/api/v1/users/register \
            -H "Content-Type: application/json" \
            -d "{\"email\":\"${ADMIN_EMAIL}\",\"password\":\"${ADMIN_PASS}\",\"username\":\"admin\",\"full_name\":\"Career-Ops Admin\"}" 2>/dev/null)
        
        if echo "$reg_response" | grep -q '"success":true\|"id"'; then
            log "✅ Admin user created!"
        else
            warn "Registration: $(echo "$reg_response" | head -c 200)"
        fi
    fi
}

# ── Phase 9: Automation ────────────────────────────────────────────────
phase_automation() {
    header "🔄 Automation Setup"
    
    # Backups
    log "Installing daily backup cron (2 AM)..."
    (crontab -l 2>/dev/null; echo "0 2 * * * cd ${PROJECT_DIR} && bash scripts/backup-db.sh --cron >> ${PROJECT_DIR}/backups/backup.log 2>&1") | crontab -
    
    log "Testing backup..."
    bash "$PROJECT_DIR/scripts/backup-db.sh" >> "$DEPLOY_LOG" 2>&1 || warn "Backup test had issues"
    
    # LinkedIn
    log "Setting up daily LinkedIn post (9 AM)..."
    mkdir -p "$PROJECT_DIR/data/linkedin"
    (crontab -l 2>/dev/null; echo "0 9 * * * cd ${PROJECT_DIR} && bash scripts/linkedin-automation.sh --daily >> ${PROJECT_DIR}/data/linkedin/poster.log 2>&1") | crontab -
    
    # n8n workflows import
    log "Importing n8n workflows..."
    if sudo docker compose exec -T n8n n8n import:workflow --separate --input=/monitoring/n8n/workflows >> "$DEPLOY_LOG" 2>&1; then
        log "✅ n8n workflows imported"
    else
        warn "n8n import skipped — import manually from monitoring/n8n/workflows/"
    fi
}

# ── Phase 10: Verification ─────────────────────────────────────────────
phase_verify() {
    header "✅ Verification"
    
    log "Running health checks..."
    
    local checks=(
        "Backend:8000/health"
        "Prometheus:9090/-/ready"
        "Grafana:3001/api/health"
    )
    
    for check in "${checks[@]}"; do
        local name="${check%%:*}"
        local url="${check#*:}"
        if curl -sf "http://localhost:${url}" > /dev/null 2>&1; then
            log "✅ ${name} is healthy"
        else
            warn "${name} not responding"
        fi
    done
    
    # Test AI
    log "Testing AI..."
    local token
    token=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"${ADMIN_EMAIL}\",\"password\":\"${ADMIN_PASS}\"}" | \
        python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('data',{}).get('access_token','') or d.get('access_token',''))" 2>/dev/null || echo "")
    
    if [ -n "$token" ]; then
        log "✅ API login working"
        
        if [ -n "$GEMINI_KEY" ]; then
            local ai_test
            ai_test=$(curl -s -X POST http://localhost:8000/api/v1/ai/ats-score \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer ${token}" \
                -d '{"resume_text":"Python developer 5 years","job_description":"Python backend engineer"}' 2>/dev/null)
            if echo "$ai_test" | grep -q "overall_score"; then
                log "✅ AI working!"
            else
                warn "AI test issue (Gemini key may need setup)"
            fi
        fi
    else
        warn "Login failed — check: docker compose logs backend"
    fi
    
    # Final Docker status
    log "Running services:"
    sudo docker compose ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null | tee /dev/fd/3
    echo "" | tee /dev/fd/3
}

# ── Phase 11: Summary ──────────────────────────────────────────────────
phase_summary() {
    header "🎉 Deployment Complete!"
    
    local vm_ip
    vm_ip=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "your-vm-ip")
    
    echo -e "${GREEN}══════════════════════════════════════════════════════${NC}" | tee /dev/fd/3
    echo -e "${BOLD}  🚀 Career-Ops v2 is LIVE!${NC}" | tee /dev/fd/3
    echo -e "${GREEN}══════════════════════════════════════════════════════${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    echo -e "  ${BOLD}Access:${NC}" | tee /dev/fd/3
    if [ "$DUCKDNS_SKIP" = false ]; then
        echo -e "  🌐  ${CYAN}https://${DUCKDNS_DOMAIN}.duckdns.org${NC}" | tee /dev/fd/3
    fi
    echo -e "  🌐  ${CYAN}http://${vm_ip}${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    echo -e "  ${BOLD}Login:${NC}" | tee /dev/fd/3
    echo -e "  📧  ${ADMIN_EMAIL}" | tee /dev/fd/3
    echo -e "  🔑  ${ADMIN_PASS}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    echo -e "  ${BOLD}Services:${NC}" | tee /dev/fd/3
    echo -e "  🚀  API:      http://${vm_ip}:8000" | tee /dev/fd/3
    echo -e "  📊  Grafana:  http://${vm_ip}:3001 (admin / ${GRAFANA_PASS})" | tee /dev/fd/3
    echo -e "  📈  Prometheus: http://${vm_ip}:9090" | tee /dev/fd/3
    echo -e "  🤖  n8n:      http://${vm_ip}:5678" | tee /dev/fd/3
    echo -e "  📖  Docs:     http://${vm_ip}:8000/docs" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    echo -e "  ${BOLD}Automation:${NC}" | tee /dev/fd/3
    echo -e "  📱  LinkedIn: ${CYAN}Daily at 9 AM${NC}" | tee /dev/fd/3
    echo -e "  💾  Backups:  ${CYAN}Daily at 2 AM${NC}" | tee /dev/fd/3
    echo -e "  🔄  DuckDNS:  ${CYAN}Every 5 minutes${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    echo -e "  ${DIM}📝 Log: ${DEPLOY_LOG}${NC}" | tee /dev/fd/3
    echo -e "  ${DIM}🔐 Credentials: ~/.careerops-credentials${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    # Save credentials
    cat > "$HOME/.careerops-credentials" << CREDEOF
╔══════════════════════════════════════════════════════════════╗
║              Career-Ops v2 — Deployment Credentials           ║
║              Deployed: ${TIMESTAMP}                           ║
╚══════════════════════════════════════════════════════════════╝

🌐 URL:       http://${vm_ip}
📧 Admin:     ${ADMIN_EMAIL}
🔑 Password:  ${ADMIN_PASS}

   $( [ "$DUCKDNS_SKIP" = false ] && echo "🌐 Domain: https://${DUCKDNS_DOMAIN}.duckdns.org" )

📊 Grafana:   http://${vm_ip}:3001 (admin / ${GRAFANA_PASS})
🤖 n8n:       http://${vm_ip}:5678
🚀 API:       http://${vm_ip}:8000
📖 Swagger:   http://${vm_ip}:8000/docs
📈 Prometheus: http://${vm_ip}:9090

💾 Backups:   ${PROJECT_DIR}/backups/
📱 LinkedIn:  ${PROJECT_DIR}/data/linkedin/
📝 Deploy log: ${DEPLOY_LOG}
CREDEOF
    chmod 600 "$HOME/.careerops-credentials"
    
    echo -e "${GREEN}══════════════════════════════════════════════════════${NC}" | tee /dev/fd/3
    echo -e "${BOLD}  🎉 Thank you! Go get that job! 🎉${NC}" | tee /dev/fd/3
    echo -e "${GREEN}══════════════════════════════════════════════════════${NC}" | tee /dev/fd/3
}

# ── Main ───────────────────────────────────────────────────────────────
main() {
    print_banner
    gather_config
    phase_system
    phase_clone
    phase_duckdns
    phase_cloudflare
    phase_telegram
    phase_deploy
    phase_init
    phase_automation
    phase_verify
    phase_summary
    
    echo "" | tee /dev/fd/3
    echo -e "${GREEN}Run: cat ~/.careerops-credentials${NC}" | tee /dev/fd/3
    echo -e "${GREEN}Or:  nano ${PROJECT_DIR}/.env${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
}

main "$@"
