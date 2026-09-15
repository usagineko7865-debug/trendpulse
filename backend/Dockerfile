# Production image for the TrendPulse backend. Build & run:
#   docker build -t trendpulse-backend .
#   docker run -p 8000:8000 --env-file .env trendpulse-backend
#
# Deploys as-is on Railway, Render, Fly.io, or any container host that
# reads a Dockerfile — no extra config needed beyond setting the env vars
# from .env.example in the platform's dashboard.
FROM python:3.12-slim

WORKDIR /app

# Install deps first so this layer is cached across code-only changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The app itself runs as a non-root user (basic container hardening).
# /app/data is a writable mount point for the SQLite file when run via
# docker-compose or Railway (DB_PATH=/app/data/trendpulse.db) — created
# here so the non-root user owns it at build time. NOTE: a platform-mounted
# persistent volume (Railway, etc.) re-attaches this path owned by root at
# container start regardless of this build-time chown, so the container
# itself stays root here and docker-entrypoint.sh re-asserts ownership
# before dropping to appuser — see that script for why.
RUN useradd --create-home appuser && mkdir -p /app/data && chown -R appuser:appuser /app

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Most hosts (Railway, Render, Fly) inject $PORT; default to 8000 for
# plain `docker run` / local use.
ENV PORT=8000
EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]
