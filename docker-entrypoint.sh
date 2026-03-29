#!/bin/sh
set -eu

MAX_RETRIES="${DB_INIT_MAX_RETRIES:-20}"
SLEEP_SECONDS="${DB_INIT_RETRY_DELAY_SECONDS:-3}"
RETRY=1

while [ "$RETRY" -le "$MAX_RETRIES" ]; do
  echo "[entrypoint] Ensuring database tables exist (attempt $RETRY/$MAX_RETRIES)..."
  if python Tables_SQL/setup_project_tables.py; then
    echo "[entrypoint] Database initialization succeeded."
    exec gunicorn -w 2 -b 0.0.0.0:5050 main:app
  fi

  echo "[entrypoint] Database not ready yet. Retrying in ${SLEEP_SECONDS}s..."
  RETRY=$((RETRY + 1))
  sleep "$SLEEP_SECONDS"
done

echo "[entrypoint] Failed to initialize database after $MAX_RETRIES attempts."
exit 1
