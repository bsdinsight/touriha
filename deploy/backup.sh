#!/usr/bin/env bash
# Backup mọi DB của stack Touriha VPS (Postgres custom-format dump + filestore).
# Chạy từ thư mục repo:
#   ./deploy/backup.sh             # backup tất cả DB
#   ./deploy/backup.sh touriha     # chỉ 1 DB
#   OUT=/mnt/backups ./deploy/backup.sh
set -euo pipefail

cd "$(dirname "$0")/.."
TS=$(date +%Y%m%d-%H%M%S)
OUT=${OUT:-/root/backups/touriha-$TS}
mkdir -p "$OUT"

compose="docker compose -f docker-compose.vps.yml"

if [[ $# -gt 0 ]]; then
    DBS="$*"
else
    DBS=$($compose exec -T db psql -U odoo -d postgres -At \
        -c "SELECT datname FROM pg_database WHERE datistemplate=false AND datname NOT IN ('postgres','odoo')")
fi

for db in $DBS; do
    echo ">> $db"
    $compose exec -T db pg_dump -U odoo -Fc "$db" > "$OUT/$db.dump"
    if [[ -d "./data/filestore/$db" ]]; then
        tar -C ./data/filestore -czf "$OUT/$db-filestore.tar.gz" "$db"
    else
        echo "   (no filestore at ./data/filestore/$db — bỏ qua tar)"
    fi
done

echo "── done → $OUT"
ls -lh "$OUT"
