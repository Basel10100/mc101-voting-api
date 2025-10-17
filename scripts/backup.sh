#!/bin/sh
set -e

STAMP=$(date +'%Y-%m-%d_%H-%M-%S')
FILE="/backups/${PGDATABASE}_${STAMP}.sql"

echo "[backup] Starting backup at $(date -Is)"
pg_dump -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" "$PGDATABASE" > "$FILE"
echo "[backup] Backup complete: $FILE"

# Optional cleanup: delete backups older than 7 days
find /backups -type f -name "*.sql" -mtime +7 -delete