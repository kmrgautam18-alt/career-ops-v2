#!/bin/bash
# =============================================================================
# Career-Ops Self-Update & Health Check Script
# =============================================================================
# Automatically checks for:
#   - Dependency updates (pip, npm, bun)
#   - New Docker image versions
#   - Security vulnerabilities
#   - Deprecated API usage
#   - Database health
#
# Usage:
#   ./scripts/self-update.sh                  # Full check
#   ./scripts/self-update.sh --check-deps     # Check dependencies only
#   ./scripts/self-update.sh --check-security # Security audit only
#   ./scripts/self-update.sh --update         # Attempt safe updates
#
# Recommended cron: 0 6 * * 1 /opt/career-ops-v2/scripts/self-update.sh
# =============================================================================

set -euo pipefail

APP_NAME="Career-Ops v2"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ── Helpers ──────────────────────────────────────────────────────────────
log()       { echo -e "[$(date '+%H:%M:%S')] $*"; }
info()      { log "${GREEN}✅${NC} $*"; }
warn()      { log "${YELLOW}⚠️${NC} $*"; }
error()     { log "${RED}❌${NC} $*"; }
header()    { echo -e "\n${CYAN}══════════════════════════════════════════════════${NC}"; echo -e "${CYAN}$*${NC}"; echo -e "${CYAN}══════════════════════════════════════════════════${NC}\n"; }
version_gt() { test "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1"; }

# ── Check Python Dependencies ──────────────────────────────────────────
check_python_deps() {
    header "🔍 Python Dependencies"

    cd "$PROJECT_DIR"
    if [ ! -f "requirements.txt" ]; then
        warn "requirements.txt not found"
        return
    fi

    # Check for outdated packages
    if command -v pip &>/dev/null; then
        pip install pip-outdated 2>/dev/null || true
        local outdated
        outdated=$(pip list --outdated --format=columns 2>/dev/null | tail -n +3 | head -20)
        if [ -n "$outdated" ]; then
            warn "Outdated Python packages:"
            echo "$outdated" | while IFS= read -r line; do
                if [ -n "$line" ]; then
                    local pkg
                    pkg=$(echo "$line" | awk '{print $1}')
                    local current
                    current=$(echo "$line" | awk '{print $2}')
                    local latest
                    latest=$(echo "$line" | awk '{print $3}')
                    echo "  - $pkg: $current → $latest"
                fi
            done
        else
            info "All Python packages up-to-date"
        fi
    fi

    # Security audit
    if command -v pip-audit &>/dev/null; then
        pip-audit --requirement requirements.txt --desc 2>&1 | head -20 || true
    fi
}

# ── Check Frontend Dependencies ────────────────────────────────────────
check_frontend_deps() {
    header "🔍 Frontend Dependencies"

    cd "$PROJECT_DIR/frontend"
    if [ ! -f "package.json" ]; then
        warn "package.json not found"
        return
    fi

    if command -v bun &>/dev/null; then
        # Check for outdated packages
        local outdated
        outdated=$(bun outdated 2>/dev/null || true)
        if echo "$outdated" | grep -qE "[0-9]+\.[0-9]+\.[0-9]+"; then
            warn "Outdated npm packages:"
            echo "$outdated" | head -15
        else
            info "All npm packages up-to-date"
        fi

        # Security audit
        local audit
        audit=$(bun audit 2>&1 || true)
        if echo "$audit" | grep -qi "critical\|high\|moderate"; then
            warn "Security vulnerabilities found!"
            echo "$audit"
        else
            info "No security vulnerabilities"
        fi
    fi
}

# ── Check Docker Images ────────────────────────────────────────────────
check_docker_images() {
    header "🔍 Docker Images"

    cd "$PROJECT_DIR"
    if [ ! -f "docker-compose.yml" ]; then
        warn "docker-compose.yml not found"
        return
    fi

    # Extract image tags from docker-compose
    local images
    images=$(grep -E '^\s+image:' docker-compose.yml | awk '{print $2}')

    if [ -z "$images" ]; then
        warn "No Docker images found"
        return
    fi

    echo "$images" | while IFS= read -r image; do
        if [ -z "$image" ]; then continue; fi
        local name="${image%:*}"
        local tag="${image##*:}"

        # Check if image exists locally
        if docker image inspect "$image" &>/dev/null; then
            local local_size
            local_size=$(docker image inspect "$image" --format='{{.Size}}' 2>/dev/null | numfmt --to=iec 2>/dev/null || echo "unknown")

            # Try to get remote digest (requires docker pull)
            if docker pull --quiet "$image" 2>/dev/null | grep -q "Downloaded"; then
                warn "Newer version available: $image"
            else
                info "$image up-to-date (${local_size})"
            fi
        else
            warn "Image not pulled: $image"
        fi
    done
}

# ── Check Database Health ──────────────────────────────────────────────
check_database() {
    header "🗄️ Database Health"

    cd "$PROJECT_DIR"
    if command -v docker &>/dev/null && docker compose ps postgres 2>/dev/null | grep -q "Up"; then
        info "PostgreSQL is running"

        # Check connection count
        local connections
        connections=$(docker compose exec -T postgres psql -U "$POSTGRES_USER" -c \
            "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';" -t 2>/dev/null | tr -d ' ')
        if [ -n "$connections" ]; then
            info "Active connections: $connections"
        fi
    else
        warn "PostgreSQL not running in Docker — check local instance"
    fi
}

# ── Security Scan ──────────────────────────────────────────────────────
check_security() {
    header "🔐 Security Scan"

    cd "$PROJECT_DIR"

    # Check for exposed secrets in code
    local secrets_found=0
    for pattern in 'sk-[a-zA-Z0-9]{20,}' 'ghp_[a-zA-Z0-9]{36}' 'AKIA[0-9A-Z]{16}' '-----BEGIN.*PRIVATE KEY-----'; do
        if grep -rl "$pattern" --include='*.py' --include='*.ts' --include='*.tsx' --include='*.js' --include='*.yml' --include='*.yaml' . 2>/dev/null \
            | grep -v node_modules | grep -v _generated | grep -v __pycache__ | grep -v '.git/' | grep -v '.env'; then
            error "Potential secret exposure found with pattern: $pattern"
            secrets_found=1
        fi
    done

    if [ "$secrets_found" -eq 0 ]; then
        info "No exposed secrets found in codebase"
    fi

    # Check .env is not committed
    if git ls-files .env --error-unmatch 2>/dev/null; then
        error ".env is tracked by git! Add to .gitignore"
    else
        info ".env is properly gitignored"
    fi

    # Check file permissions on sensitive files
    for f in ".env" ".env.production" "monitoring/alertmanager/alertmanager.yml"; do
        if [ -f "$f" ] && [ "$(stat -c "%a" "$f" 2>/dev/null)" -gt "600" ]; then
            warn "Permissions too permissive on $f: $(stat -c '%a' "$f")"
        fi
    done
}

# ── API Deprecation Check ──────────────────────────────────────────────
check_deprecations() {
    header "📋 API & Framework Deprecation Check"

    cd "$PROJECT_DIR"

    # Python version
    local py_ver
    py_ver=$(python3 --version 2>&1 | awk '{print $2}')
    if version_gt "3.13" "$py_ver"; then
        info "Python $py_ver is supported until 2028+"
    else
        warn "Python $py_ver — check end-of-life schedule"
    fi

    # FastAPI version
    if command -v python3 &>/dev/null; then
        local fastapi_ver
        fastapi_ver=$(python3 -c "import fastapi; print(fastapi.__version__)" 2>/dev/null || echo "unknown")
        if [ "$fastapi_ver" != "unknown" ]; then
            info "FastAPI $fastapi_ver"
        fi
    fi

    # Check for deprecated dependencies in requirements
    if [ -f "requirements.txt" ]; then
        local deprecated_pkgs=""
        for pkg in pylint pyflakes; do
            if grep -qi "^${pkg}" requirements.txt 2>/dev/null; then
                deprecated_pkgs="$deprecated_pkgs $pkg"
            fi
        done
        if [ -n "$deprecated_pkgs" ]; then
            warn "Deprecated packages found:$deprecated_pkgs"
        fi
    fi
}

# ── Update Dependencies (Safe) ─────────────────────────────────────────
do_update() {
    header "🔄 Attempting Safe Updates"

    cd "$PROJECT_DIR"

    # Backup requirements first
    if [ -f "requirements.txt" ]; then
        cp requirements.txt requirements.txt.bak
        info "Backed up requirements.txt"
    fi

    # Update Python packages
    if command -v pip &>/dev/null; then
        info "Updating Python packages..."
        pip install --upgrade pip setuptools wheel 2>/dev/null || true
        pip list --outdated --format=freeze 2>/dev/null | grep -v '^\-e' | cut -d= -f1 | \
            xargs -r pip install --upgrade 2>/dev/null || true
        # Regenerate requirements
        pip freeze > requirements.txt 2>/dev/null || true
        info "Python packages updated"
    fi

    # Update frontend packages
    if command -v bun &>/dev/null && [ -f "frontend/package.json" ]; then
        cd frontend
        bun update 2>/dev/null || true
        cd "$PROJECT_DIR"
        info "Frontend packages updated"
    fi

    info "Update complete! Review changes before committing."
}

# ── Main ──────────────────────────────────────────────────────────────
main() {
    echo -e "${CYAN}"
    echo "  ╔═══════════════════════════════════════════╗"
    echo "  ║      ${APP_NAME} — Self-Update            ║"
    echo "  ║      ${TIMESTAMP}        ║"
    echo "  ╚═══════════════════════════════════════════╝"
    echo -e "${NC}"

    local action="${1:---full}"

    case "$action" in
        --full|-f|"")
            check_python_deps
            check_frontend_deps
            check_docker_images
            check_database
            check_security
            check_deprecations
            echo -e "\n${GREEN}══════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}  ✅ Self-check complete. Review any warnings above.${NC}"
            echo -e "${GREEN}══════════════════════════════════════════════════${NC}"
            ;;
        --check-deps)
            check_python_deps
            check_frontend_deps
            ;;
        --check-security)
            check_security
            ;;
        --check-docker)
            check_docker_images
            ;;
        --check-db)
            check_database
            ;;
        --update)
            do_update
            ;;
        --help|-h)
            echo "Usage: $0 [action]"
            echo ""
            echo "Actions:"
            echo "  (no args)       Full self-check (deps, security, docker, db)"
            echo "  --check-deps    Check dependency versions only"
            echo "  --check-security Check for exposed secrets and security issues"
            echo "  --check-docker  Check Docker image versions"
            echo "  --check-db      Check database health"
            echo "  --update        Attempt safe dependency updates"
            echo "  --help          Show this help"
            ;;
        *)
            error "Unknown action: $action"
            echo "Usage: $0 [--check-deps|--check-security|--check-docker|--check-db|--update|--help]"
            exit 1
            ;;
    esac
}

main "$@"
