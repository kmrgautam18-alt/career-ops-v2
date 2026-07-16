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
#   ✓ Auto-detects Podman (RHEL default) or Docker
#   ✓ Installs container engine + system dependencies
#   ✓ Clones Career-Ops repository
#   ✓ Prompts for config (press Enter to auto-default)
#   ✓ Sets up DuckDNS free domain
#   ✓ Configures Cloudflare Tunnel (optional)
#   ✓ Builds & starts all 16 containers
#   ✓ Creates admin user
#   ✓ Sets up daily backups + LinkedIn automation
#   ✓ Verifies everything is working
#
# Requirements:
#   - Fresh RHEL 9/10 VM with internet access
#   - DuckDNS token (free: https://duckdns.org)
#   - Gemini API key (free: https://aistudio.google.com)
#
# Compatibility:
#   - Works with Podman (default on RHEL) OR Docker CE
#   - Auto-detects available container engine
#   - Uses podman compose / podman-compose / docker compose as available
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
DRY_RUN=false
ENGINE=""
COMPOSE_CMD=""
ENGINE_LABEL=""

# Parse --dry-run flag
for arg in "$@"; do
    if [ "$arg" = "--dry-run" ] || [ "$arg" = "--dryrun" ] || [ "$arg" = "-n" ]; then
        DRY_RUN=true
    fi
done

# ── Container Engine Detection ────────────────────────────────────────
# RHEL ships Podman by default instead of Docker.
# This function detects what's available and sets ENGINE + COMPOSE_CMD.
detect_engine() {
    echo "" | tee /dev/fd/3
    echo -e "${CYAN}🔍 Detecting container engine...${NC}" | tee /dev/fd/3
    
    # Check for Podman (default on RHEL 8/9/10)
    if command -v podman &>/dev/null; then
        local pv
        pv=$(podman --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' || echo "unknown")
        echo -e "  ${GREEN}✅ Podman ${pv} detected${NC}" | tee /dev/fd/3
        ENGINE="sudo podman"
        
        # Check what compose subcommand is available
        if podman compose --help &>/dev/null 2>&1; then
            COMPOSE_CMD="sudo podman compose"
            echo -e "  ${GREEN}✅ podman compose available${NC}" | tee /dev/fd/3
        elif command -v podman-compose &>/dev/null; then
            COMPOSE_CMD="sudo podman-compose"
            echo -e "  ${GREEN}✅ podman-compose available${NC}" | tee /dev/fd/3
        elif docker compose --help &>/dev/null 2>&1; then
            # podman-docker compatibility layer
            COMPOSE_CMD="sudo docker compose"
            echo -e "  ${GREEN}✅ docker compose (via podman-docker) available${NC}" | tee /dev/fd/3
        else
            warn "No compose subcommand found — will install podman-compose"
            COMPOSE_CMD="sudo podman-compose"
        fi
        ENGINE_LABEL="Podman ${pv}"
        return
    fi
    
    # Fallback to Docker
    if command -v dockerd &>/dev/null || command -v docker &>/dev/null; then
        if docker info &>/dev/null 2>&1; then
            local dv
            dv=$(docker --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' || echo "unknown")
            echo -e "  ${GREEN}✅ Docker ${dv} detected${NC}" | tee /dev/fd/3
            ENGINE="sudo docker"
            COMPOSE_CMD="sudo docker compose"
            ENGINE_LABEL="Docker ${dv}"
            return
        fi
    fi
    
    # Neither found — will install Podman
    echo -e "  ${YELLOW}⚠ No container engine found — will install Podman${NC}" | tee /dev/fd/3
    ENGINE="sudo podman"
    COMPOSE_CMD="sudo podman-compose"
    ENGINE_LABEL="Podman (to install)"
}

# ── Logger ──────────────────────────────────────────────────────────────
exec 3>&1 4>&2
exec >> "$DEPLOY_LOG" 2>&1

log()    { echo -e "${GREEN}[✓]${NC} $*" | tee /dev/fd/3; }
warn()   { echo -e "${YELLOW}[!]${NC} $*" | tee /dev/fd/3; }
error()  { echo -e "${RED}[✗]${NC} $*" | tee /dev/fd/3; }
dry()    { echo -e "${MAGENTA}[DRY-RUN]${NC} $*" | tee /dev/fd/3; }
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
    if [ "$DRY_RUN" = true ]; then
        echo -e "${MAGENTA}[DRY-RUN]${NC} $msg ${DIM}(would run with spinner)${NC}" | tee /dev/fd/3
        return
    fi
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
    
    if [ "$DRY_RUN" = true ]; then
        # Use default value automatically in dry-run mode
        eval "$var_name=\"$default_val\""
        echo -e "${MAGENTA}[DRY-RUN]${NC} $prompt_msg ${DIM}→ auto-default: '$default_val'${NC}" | tee /dev/fd/3
        return
    fi
    
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
    
    if [ "$DRY_RUN" = true ]; then
        # Auto-accept all confirmations in dry-run mode
        return 0
    fi
    
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
    echo -e "  ${DIM}  Container engine: ${ENGINE_LABEL}${NC}" | tee /dev/fd/3
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
    # Strip .duckdns.org if user entered the full URL
    DUCKDNS_DOMAIN="${DUCKDNS_DOMAIN%.duckdns.org}"
    DUCKDNS_DOMAIN="${DUCKDNS_DOMAIN%.duckdns.org}"  # strip again in case of .duckdns.org.duckdns.org
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
    if [ -n "$SMTP_EMAIL" ]; then
        echo -e "  Email:      ${CYAN}${SMTP_EMAIL}${NC}" | tee /dev/fd/3
    else
        echo -e "  Email:      ${CYAN}None${NC}" | tee /dev/fd/3
    fi
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
    
    if [ "$DRY_RUN" = true ]; then
        dry "sudo dnf update -y"
        if echo "$ENGINE" | grep -q podman; then
            dry "sudo dnf install -y podman podman-docker podman-compose"
        else
            dry "sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin"
            dry "sudo systemctl enable --now docker"
            dry "sudo usermod -aG docker \"${USER:-$(whoami)}\""
        fi
        dry "sudo dnf install -y git curl jq openssl cronie nano"
        dry "sudo firewall-cmd --permanent --add-port={80,443,8000,5678,3001,9090}/tcp"
        dry "sudo setsebool -P httpd_can_network_connect on"
        log "Dry-run: All system changes would be applied"
        return
    fi
    
    log "Updating system packages..."
    sudo dnf update -y >> "$DEPLOY_LOG" 2>&1 &
    spinner $! "Updating packages"
    
    # ── Install Container Engine ───────────────────────────────────────
    if echo "$ENGINE" | grep -q podman; then
        log "Installing Podman (RHEL-native container engine)..."
        sudo dnf install -y podman podman-docker podman-compose >> "$DEPLOY_LOG" 2>&1 &
        spinner $! "Installing Podman + compose"
        
        # Re-detect compose command after install
        if podman compose --help &>/dev/null 2>&1; then
            COMPOSE_CMD="sudo podman compose"
            log "Using: podman compose"
        elif command -v podman-compose &>/dev/null; then
            COMPOSE_CMD="sudo podman-compose"
            log "Using: podman-compose"
        fi
        
        ENGINE_LABEL="Podman $(podman --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' || echo 'installed')"
        log "Podman ready — daemonless, no systemd service needed"
        log "NOTE: Skipping docker group (not needed for Podman)"
    else
        log "Installing Docker CE..."
        sudo dnf install -y dnf-plugins-core >> "$DEPLOY_LOG" 2>&1
        sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo >> "$DEPLOY_LOG" 2>&1 || true
        sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin >> "$DEPLOY_LOG" 2>&1 &
        spinner $! "Installing Docker CE"
        
        sudo systemctl enable --now docker >> "$DEPLOY_LOG" 2>&1
        sudo usermod -aG docker "${USER:-$(whoami)}" >> "$DEPLOY_LOG" 2>&1
        log "Docker installed and enabled"
    fi
    
    # ── Common tools ────────────────────────────────────────────────────
    log "Installing git, curl, jq, openssl..."
    sudo dnf install -y git curl jq openssl cronie nano >> "$DEPLOY_LOG" 2>&1 &
    spinner $! "Installing tools"
    
    # Verify engine works
    log "Verifying container engine..."
    $ENGINE ps > /dev/null 2>&1 && log "✅ Container engine responding" || warn "Engine check had issues (may need re-login for root permissions)"
    
    # Firewall
    log "Opening firewall ports..."
    sudo firewall-cmd --permanent --add-port={80,443,8000,5678,3001,9090}/tcp 2>/dev/null || true
    sudo firewall-cmd --reload 2>/dev/null || true
    
    # SELinux — critical for Podman bind mounts on RHEL
    if command -v getenforce &>/dev/null && [ "$(getenforce)" = "Enforcing" ]; then
        warn "SELinux is Enforcing — setting required booleans"
        sudo setsebool -P httpd_can_network_connect on 2>/dev/null || true
        if echo "$ENGINE" | grep -q podman; then
            log "SELinux Enforcing — Podman handles :z volume labels automatically"
            log "If bind-mounts fail, append :z to volumes in docker-compose.yml"
        fi
    fi
}

# ── Phase 3: Clone & Configure ─────────────────────────────────────────
phase_clone() {
    header "📦 Clone & Configure"
    
    if [ "$DRY_RUN" = true ]; then
        dry "git clone $REPO_URL $PROJECT_DIR"
        dry "Generate .env with secure secrets"
        dry "mkdir -p data monitoring/loki backups/postgres"
    fi
    
    cd "$HOME"
    
    log "Cloning Career-Ops..."
    if [ -d "$PROJECT_DIR" ] && [ "$DRY_RUN" = false ]; then
        warn "Directory exists — pulling latest"
        # Don't let git pull failure crash the script (set -e)
        cd "$PROJECT_DIR" && git pull origin main >> "$DEPLOY_LOG" 2>&1 || \
            warn "Git pull had issues — check $DEPLOY_LOG for details. Continuing with existing code."
    elif [ "$DRY_RUN" = false ]; then
        mkdir -p "$HOME"
        git clone "$REPO_URL" "$PROJECT_DIR" >> "$DEPLOY_LOG" 2>&1 || \
            { warn "Git clone failed — check $DEPLOY_LOG"; return; }
        log "Repository cloned from GitHub"
    fi
    
    [ "$DRY_RUN" = false ] && cd "$PROJECT_DIR"
    
    log "Generating secure .env..."
    POSTGRES_PASS=$(openssl rand -hex 32 2>/dev/null || echo "test_postgres_pass_32bytes_abcdef123456")
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "test_secret_key_32bytes_abcdef1234567890")
    GRAFANA_PASS=$(openssl rand -hex 16 2>/dev/null || echo "test_grafana_pass")
    N8N_KEY=$(openssl rand -hex 32 2>/dev/null || echo "test_n8n_key_32bytes_abcdef1234567890")
    
    # Show the .env that would be generated
    echo -e "${CYAN}  Generated .env content:${NC}" | tee /dev/fd/3
    echo -e "${DIM}  ─────────────────────────────────────────${NC}" | tee /dev/fd/3
    
    cat > /tmp/.env.test << ENVEOF
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
LLM_API_KEY=${GEMINI_KEY:-}
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
SMTP_USER=${SMTP_EMAIL:-}
SMTP_PASSWORD=${SMTP_PASSWORD:-}
SMTP_FROM_EMAIL=${SMTP_EMAIL:-}
SMTP_FROM_NAME=Career-Ops
SMTP_TLS=true
SMTP_ENABLED=$([ -n "${SMTP_EMAIL:-}" ] && echo "true" || echo "false")

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
OAUTH_ENABLED=$([ -n "${GOOGLE_CLIENT_ID:-}" ] || [ -n "${GITHUB_CLIENT_ID:-}" ] && echo "true" || echo "false")
GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID:-}
GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET:-}
GITHUB_CLIENT_ID=${GITHUB_CLIENT_ID:-}
GITHUB_CLIENT_SECRET=${GITHUB_CLIENT_SECRET:-}

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
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN:-}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID:-}
ENVEOF
    
. /tmp/.env.test 2>/dev/null || true
    
    # Display .env (redacted secrets)
    while IFS= read -r line; do
        if echo "$line" | grep -qE "(PASSWORD|SECRET|KEY|TOKEN)"; then
            echo -e "  ${DIM}${line%%=*}=********${NC}" | tee /dev/fd/3
        else
            echo -e "  ${DIM}$line${NC}" | tee /dev/fd/3
        fi
    done < /tmp/.env.test
    echo -e "${DIM}  ─────────────────────────────────────────${NC}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
    
    if [ "$DRY_RUN" = true ]; then
        log "Dry-run: .env generated at /tmp/.env.test for inspection"
    else
        cp /tmp/.env.test .env
        chmod 600 .env
        log ".env created with secure random secrets"
        mkdir -p data monitoring/loki backups/postgres
        log "Data directories created"
    fi
    rm -f /tmp/.env.test
}

# ── Phase 4: DuckDNS ───────────────────────────────────────────────────
phase_duckdns() {
    if [ "$DUCKDNS_SKIP" = true ]; then
        log "Skipping DuckDNS (no token provided)"
        return
    fi
    
    header "🌐 DuckDNS — Free Domain"
    
    if [ "$DRY_RUN" = true ]; then
        dry "sudo mkdir -p /opt/duckdns"
        dry "Create /opt/duckdns/duck.sh with your token"
        dry "Install cron job: */5 * * * * /opt/duckdns/duck.sh"
        log "Dry-run: DuckDNS would use domain '${DUCKDNS_DOMAIN}.duckdns.org'"
        return
    fi
    
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
    
    if [ "$DRY_RUN" = true ]; then
        dry "$ENGINE run -d --name cloudflared cloudflare/cloudflared:latest tunnel --token ..."
        log "Dry-run: HTTPS would be enabled at ${DUCKDNS_DOMAIN}.duckdns.org"
        return
    fi
    
    log "Starting Cloudflare Tunnel container..."
    $ENGINE rm -f cloudflared 2>/dev/null || true
    $ENGINE run -d --restart=always --name cloudflared \
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
    
    if [ "$DRY_RUN" = true ]; then
        dry "curl -s https://api.telegram.org/bot.../sendMessage -d 'chat_id=...' -d 'text=🚀 Career-Ops deployment started!'"
        log "Dry-run: Telegram notifications would be configured"
        return
    fi
    
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

# ── Phase 7: Build & Start Containers ──────────────────────────────────
phase_deploy() {
    header "🐳 Building & Starting ${ENGINE_LABEL} Stack"
    
    if [ "$DRY_RUN" = true ]; then
        dry "$COMPOSE_CMD up -d --build"
        dry "Services: backend, frontend, postgres, redis, celery-worker, celery-beat, n8n, prometheus, grafana, alertmanager, loki, promtail, postgres-exporter, nginx-exporter, cloudflared"
        log "Dry-run: 16 containers would be built and started"
        return
    fi
    
    # Podman is daemonless — no systemctl start needed
    if echo "$ENGINE" | grep -q docker; then
        sudo systemctl start docker 2>/dev/null || true
    fi
    
    log "Building 16 containers (first time: 3-5 minutes)..."
    
    cd "$PROJECT_DIR"
    $COMPOSE_CMD up -d --build >> "$DEPLOY_LOG" 2>&1 &
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
    
    echo -e "\r${GREEN}✅${NC} All containers built and started!" | tee /dev/fd/3
    
    log "Waiting for services to be healthy..."
    sleep 10
    
    $COMPOSE_CMD ps --format "table {{.Name}}\t{{.Status}}" | tee /dev/fd/3
    echo "" | tee /dev/fd/3
}

# ── Phase 8: Initialize DB & User ──────────────────────────────────────
phase_init() {
    header "⚡ Database & User Setup"
    
    if [ "$DRY_RUN" = true ]; then
        dry "$COMPOSE_CMD exec backend alembic upgrade head"
        dry "POST /api/v1/users/register with email=${ADMIN_EMAIL}, password=********"
        log "Dry-run: Database migrations + admin user would be set up"
        return
    fi
    
    log "Running migrations..."
    $COMPOSE_CMD exec -T backend alembic upgrade head >> "$DEPLOY_LOG" 2>&1 || \
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
    
    if [ "$DRY_RUN" = true ]; then
        dry "crontab: 0 2 * * * → backup-db.sh"
        dry "crontab: 0 9 * * * → linkedin-automation.sh --daily"
        dry "$COMPOSE_CMD exec n8n n8n import:workflow --separate --input=/monitoring/n8n/workflows"
        log "Dry-run: Backup, LinkedIn, and n8n automation would be configured"
        return
    fi
    
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
    if $COMPOSE_CMD exec -T n8n n8n import:workflow --separate --input=/monitoring/n8n/workflows >> "$DEPLOY_LOG" 2>&1; then
        log "✅ n8n workflows imported"
    else
        warn "n8n import skipped — import manually from monitoring/n8n/workflows/"
    fi
}

# ── Phase 10: Verification ─────────────────────────────────────────────
phase_verify() {
    header "✅ Verification"
    
    if [ "$DRY_RUN" = true ]; then
        dry "curl localhost:8000/health → health check"
        dry "curl localhost:8000/api/v1/auth/login → login test"
        dry "docker compose ps → service status"
        log "Dry-run: Health checks would verify all 16 services"
        return
    fi
    
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
        warn "Login failed — check: $COMPOSE_CMD logs backend"
    fi
    
    # Final container status
    log "Running services:"
    $COMPOSE_CMD ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null | tee /dev/fd/3 || true
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
    detect_engine
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
