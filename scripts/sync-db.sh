#!/usr/bin/env bash
#
# Sync production database to local dev database.
#
# Reads DATABASE_URL from .env (production), dumps it with pg_dump,
# then restores into the local PostgreSQL instance.
#
# Usage:
#   ./scripts/sync-db.sh
#

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$PROJECT_DIR/.env"

TARGET_USER="postgres"
TARGET_DB="caten_music"
TARGET_HOST="localhost"
TARGET_PORT="5432"

# ── 1. Read DATABASE_URL from .env ──────────────────

if [[ ! -f "$ENV_FILE" ]]; then
    echo "Error: .env not found at $ENV_FILE"
    exit 1
fi

SOURCE_URL=$(grep -m1 '^DATABASE_URL=' "$ENV_FILE" | cut -d= -f2-)

if [[ -z "${SOURCE_URL:-}" ]]; then
    echo "Error: DATABASE_URL is not set in .env"
    exit 1
fi

# Strip SQLAlchemy async driver suffix (e.g. +asyncpg)
SOURCE_URL="${SOURCE_URL//+asyncpg/}"

MASKED=$(echo "$SOURCE_URL" | sed -E 's|(://[^:]*:)[^@]*@|\1****@|')
echo "Source: $MASKED"
echo "Target: $TARGET_HOST:$TARGET_PORT/$TARGET_DB"

# ── 2. Reset target database ────────────────────────

echo "Resetting $TARGET_DB..."

psql -U "$TARGET_USER" -h "$TARGET_HOST" -p "$TARGET_PORT" -d postgres -c \
    "SELECT pg_terminate_backend(pid)
     FROM pg_stat_activity
     WHERE datname = '$TARGET_DB' AND pid <> pg_backend_pid();" \
    &>/dev/null || true

psql -U "$TARGET_USER" -h "$TARGET_HOST" -p "$TARGET_PORT" -d postgres -c \
    "DROP DATABASE IF EXISTS $TARGET_DB;"

psql -U "$TARGET_USER" -h "$TARGET_HOST" -p "$TARGET_PORT" -d postgres -c \
    "CREATE DATABASE $TARGET_DB;"

# ── 3. Dump from production & restore locally ───────

echo "Dumping and restoring..."
# Drop the default public schema so pg_dump's CREATE SCHEMA doesn't conflict
psql -U "$TARGET_USER" -h "$TARGET_HOST" -p "$TARGET_PORT" -d "$TARGET_DB" -c \
    "DROP SCHEMA IF EXISTS public CASCADE;"

pg_dump --no-owner --no-privileges --schema=public "$SOURCE_URL" \
    | psql -U "$TARGET_USER" -h "$TARGET_HOST" -p "$TARGET_PORT" -d "$TARGET_DB" -q

echo "Done. Local database is now in sync with production."
