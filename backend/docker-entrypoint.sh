#!/bin/sh
set -e

# A platform-mounted persistent volume (e.g. Railway) is attached owned by
# root regardless of the ownership baked into the image at build time —
# discovered the hard way: sqlite3 could not open/create its file on the
# volume and every deploy silently ran on a fresh, empty database. Re-assert
# ownership on whatever directory DB_PATH lives in (as root, before we drop
# privileges below) so the non-root app user can actually write there.
if [ -n "$DB_PATH" ]; then
  DB_DIR=$(dirname "$DB_PATH")
  mkdir -p "$DB_DIR"
  chown -R appuser:appuser "$DB_DIR" 2>/dev/null || true
fi

exec su -s /bin/sh appuser -c "uvicorn main:app --host 0.0.0.0 --port ${PORT}"
