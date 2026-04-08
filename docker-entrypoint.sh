#!/bin/sh
set -eu

MAX_RETRIES="${DB_INIT_MAX_RETRIES:-20}"
SLEEP_SECONDS="${DB_INIT_RETRY_DELAY_SECONDS:-3}"
RETRY=1

echo "[entrypoint] Ensuring database tables exist..."
# Database initialization is now handled by PostgreSQL via init.sql mount.
echo "[entrypoint] Database initialization via container complete."
exec gunicorn -w 2 -b 0.0.0.0:5050 main:app

echo "[entrypoint] Failed to initialize database after $MAX_RETRIES attempts."
exit 1
