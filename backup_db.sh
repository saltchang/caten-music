#!/bin/bash

usage() {
    echo "Usage: $0 --database-url <DATABASE_URL> [--backup-dir <BACKUP_DIR>]"
    echo
    echo "Options:"
    echo "  --database-url  PostgreSQL connection URL (required)"
    echo "  --backup-dir    Backup directory (optional, defaults to ./backups)"
    echo
    echo "Example:"
    echo "  $0 --database-url 'postgres://user:pass@host/dbname' --backup-dir '/path/to/backups'"
    exit 1
}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export TZ='Asia/Taipei'

while [[ $# -gt 0 ]]; do
    case $1 in
        --database-url)
            DATABASE_URL="$2"
            shift 2
            ;;
        --backup-dir)
            BACKUP_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown parameter: $1"
            usage
            ;;
    esac
done

if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL is required"
    usage
fi

backup_dir="${BACKUP_DIR:-$SCRIPT_DIR/backups}"
mkdir -p "$backup_dir"

timestamp=$(date +%Y%m%d_%H%M%S_%Z%z)
backup_file="${backup_dir}/backup_${timestamp}.sql"

pg_dump "$DATABASE_URL" > "$backup_file"

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $backup_file"
else
    echo "Backup failed!"
    exit 1
fi
