#!/bin/bash
# =============================================================================
# Career-Ops Database Backup Script
# =============================================================================
# Usage:
#   ./scripts/backup-db.sh                    # Manual backup
#   ./scripts/backup-db.sh --cron              # Cron-friendly (no prompts)
#   ./scripts/backup-db.sh --restore <file>    # Restore from backup
#   ./scripts/backup-db.sh --list              # List available backups
#   ./scripts/backup-db.sh --cleanup           # Remove old backups
#
# Scheduled via crontab:
#   0 2 * * * /opt/career-ops-v2/scripts/backup-db.sh --cron
# =============================================================================

set -euo pipefail

APP_NAME="careerops"
BACKUP_DIR="${BACKUP_DIR:-./backups/postgres}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${BACKUP_DIR}/backup.log"

# ── Colors ─────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ── Helpers ──────────────────────────────────────────────────────────────
log() {
    local level=$1
    shift
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [${level}] $*"
    echo -e "$msg" | tee -a "$LOG_FILE"
}

info()    { log "INFO"    "${GREEN}$*${NC}"; }
warn()    { log "WARNING" "${YELLOW}$*${NC}"; }
error()   { log "ERROR"   "${RED}$*${NC}"; }
header()  { echo -e "\n${CYAN}═══ $* ═══${NC}\n"; }

# ── Prerequisites ──────────────────────────────────────────────────────
check_prereqs() {
    local missing=0
    for cmd in pg_dump pg_restore gzip docker; do
        if ! command -v "$cmd" &>/dev/null; then
            error "Missing prerequisite: $cmd"
            missing=1
        fi
    done

    if [ ! -f ".env" ] && [ ! -f ".env.production" ]; then
        warn "No .env or .env.production found — using defaults"
    fi

    if [ "$missing" -eq 1 ]; then
        error "Install missing prerequisites and try again"
        exit 1
    fi
}

# ── Get DB URL ─────────────────────────────────────────────────────────
get_db_url() {
    local url="${DATABASE_URL:-}"

    if [ -z "$url" ] && [ -f ".env" ]; then
        url=$(grep -E '^DATABASE_URL=' .env | cut -d= -f2- | tr -d '"')
    fi

    if [ -z "$url" ] && [ -f ".env.production" ]; then
        url=$(grep -E '^DATABASE_URL=' .env.production | cut -d= -f2- | tr -d '"')
    fi

    # Fallback: extract from docker-compose
    if [ -z "$url" ] && command -v docker &>/dev/null; then
        if docker compose ps postgres 2>/dev/null | grep -q "Up"; then
            local user="${POSTGRES_USER:-careerops}"
            local password="${POSTGRES_PASSWORD:-}"
            local db="${POSTGRES_DB:-careerops}"
            url="postgresql://${user}:${password}@localhost:5432/${db}"
        fi
    fi

    echo "$url"
}

# ── Backup ──────────────────────────────────────────────────────────────
do_backup() {
    header "Backing up ${APP_NAME} database"

    mkdir -p "$BACKUP_DIR"

    local db_url
    db_url=$(get_db_url)

    if [ -z "$db_url" ]; then
        error "Cannot determine DATABASE_URL"
        error "Set DATABASE_URL env var or ensure .env file exists"
        exit 1
    fi

    local backup_file="${BACKUP_DIR}/${APP_NAME}_${TIMESTAMP}.sql.gz"
    local checksum_file="${backup_file}.sha256"

    info "Database URL: $(echo "$db_url" | sed 's|://[^:]*:[^@]*|://***:***@|')"
    info "Backup file: $backup_file"

    # Perform backup
    if pg_dump "$db_url" --no-owner --no-acl --compress=9 \
        --file="$backup_file" 2>&1; then
        info "✅ Backup completed: $(du -h "$backup_file" | cut -f1)"

        # Generate checksum
        sha256sum "$backup_file" > "$checksum_file"
        info "Checksum: $(cut -d' ' -f1 < "$checksum_file")"

        # Test backup integrity
        if gzip -t "$backup_file" 2>/dev/null; then
            info "✅ Backup integrity verified"
        else
            error "❌ Backup integrity check FAILED"
            rm -f "$backup_file" "$checksum_file"
            exit 1
        fi

        # Cleanup old backups
        do_cleanup
    else
        error "❌ Backup FAILED"
        rm -f "$backup_file" 2>/dev/null
        exit 1
    fi
}

# ── Restore ──────────────────────────────────────────────────────────────
do_restore() {
    local restore_file="$1"

    if [ ! -f "$restore_file" ]; then
        error "Backup file not found: $restore_file"
        exit 1
    fi

    header "Restoring from $restore_file"

    local db_url
    db_url=$(get_db_url)

    if [ -z "$db_url" ]; then
        error "Cannot determine DATABASE_URL"
        exit 1
    fi

    # Warn about destructive action
    if [ "${2:-}" != "--force" ]; then
        echo -e "${RED}⚠️  DESTRUCTIVE ACTION: This will REPLACE the current database!${NC}"
        echo -n "Are you sure? (type 'yes' to confirm): "
        read -r confirm
        if [ "$confirm" != "yes" ]; then
            info "Restore cancelled."
            exit 0
        fi
    fi

    info "Dropping and recreating database..."
    createdb "${APP_NAME}_new" 2>/dev/null || true

    info "Restoring from backup..."
    if gunzip -c "$restore_file" | pg_restore "$db_url" --no-owner --no-acl \
        --clean --if-exists 2>&1; then
        info "✅ Database restored successfully from $restore_file"
    else
        error "❌ Restore FAILED — database may be in inconsistent state"
        exit 1
    fi
}

# ── List Backups ───────────────────────────────────────────────────────
do_list() {
    header "Available Backups"

    if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A "$BACKUP_DIR"/*.sql.gz 2>/dev/null)" ]; then
        info "No backups found in $BACKUP_DIR"
        exit 0
    fi

    echo -e "${CYAN}Date                    Size        File${NC}"
    echo "────────────────────────────────────────────────────────────"
    for f in $(ls -tr "$BACKUP_DIR"/*.sql.gz 2>/dev/null); do
        local size
        size=$(du -h "$f" | cut -f1)
        local date_str
        date_str=$(date -r "$f" '+%Y-%m-%d %H:%M:%S')
        local name
        name=$(basename "$f")
        echo -e " ${date_str}  ${size}  ${name}"
    done
    echo ""
    info "$(ls "$BACKUP_DIR"/*.sql.gz 2>/dev/null | wc -l) backup(s) total"
    info "Backup directory: $(realpath "$BACKUP_DIR")"
}

# ── Cleanup Old Backups ──────────────────────────────────────────────
do_cleanup() {
    if [ ! -d "$BACKUP_DIR" ]; then
        return
    fi

    local count=0
    while IFS= read -r -d '' f; do
        rm -f "$f" "${f}.sha256"
        count=$((count + 1))
    done < <(find "$BACKUP_DIR" -name "*.sql.gz" -mtime "+${RETENTION_DAYS}" -print0)

    if [ "$count" -gt 0 ]; then
        info "Cleaned up ${count} backup(s) older than ${RETENTION_DAYS} days"
    fi
}

# ── Main ──────────────────────────────────────────────────────────────
main() {
    local action="${1:-backup}"

    case "$action" in
        backup|--backup)
            check_prereqs
            do_backup
            ;;
        --cron)
            check_prereqs
            do_backup 2>&1 | logger -t "${APP_NAME}-backup"
            ;;
        restore|--restore)
            if [ -z "${2:-}" ]; then
                error "Usage: $0 --restore <backup_file> [--force]"
                do_list
                exit 1
            fi
            check_prereqs
            do_restore "$2" "${3:-}"
            ;;
        list|--list)
            do_list
            ;;
        cleanup|--cleanup)
            do_cleanup
            info "Cleanup complete"
            ;;
        help|--help|-h)
            echo "Usage: $0 <action>"
            echo ""
            echo "Actions:"
            echo "  backup              Create a new backup (default)"
            echo "  --cron              Run backup silently (for cron jobs)"
            echo "  restore <file>      Restore from backup file"
            echo "  list                List all backups"
            echo "  cleanup             Remove backups older than ${RETENTION_DAYS} days"
            echo "  help                Show this help"
            ;;
        *)
            error "Unknown action: $action"
            echo "Usage: $0 <backup|restore|list|cleanup|help>"
            exit 1
            ;;
    esac
}

main "$@"
