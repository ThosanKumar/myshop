#!/usr/bin/env bash
# Export a static snapshot of the local Django site using wget
# Usage: ./scripts/export_static.sh [PORT]

PORT=${1:-8000}
ROOT_URL="http://127.0.0.1:${PORT}/"
OUT_DIR="export/${PORT}"

set -euo pipefail

echo "Starting Django dev server on port ${PORT}..."
export DJANGO_SETTINGS_MODULE=myshop.settings
python manage.py migrate --noinput || true &
python manage.py collectstatic --noinput || true
nohup python manage.py runserver 0.0.0.0:${PORT} &
SERVER_PID=$!
echo "Dev server PID: ${SERVER_PID}"

sleep 2

echo "Mirroring ${ROOT_URL} into ${OUT_DIR}"
rm -rf "${OUT_DIR}"
mkdir -p "${OUT_DIR}"
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --directory-prefix="${OUT_DIR}" "${ROOT_URL}"

echo "Killing dev server ${SERVER_PID}"
kill ${SERVER_PID} || true

echo "Static export complete: ${OUT_DIR}"
