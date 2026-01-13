#!/usr/bin/env sh
set -eu

# Basic wait-for-db (no extra deps)
if [ "${POSTGRES_HOST:-}" != "" ]; then
  echo "Waiting for DB at ${POSTGRES_HOST}:${POSTGRES_PORT:-5432}..."
  for i in $(seq 1 30); do
    if (echo > /dev/tcp/${POSTGRES_HOST}/${POSTGRES_PORT:-5432}) >/dev/null 2>&1; then
      echo "DB is reachable."
      break
    fi
    sleep 1
  done
fi

exec "$@"
