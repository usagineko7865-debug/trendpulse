"""Centralized environment configuration. Fails loudly (not silently) if a
required secret is missing at the point it's actually needed, so the app can
still boot in dev without every key set (e.g. to serve the LP while the
newsletter pipeline is unconfigured)."""
import os
from functools import lru_cache


class Settings:
    # --- AI content generation (Anthropic) ---
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-8")

    # --- Trend data source (YouTube Data API v3 — real data, not simulated) ---
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    TREND_REGION_CODES: list[str] = os.getenv("TREND_REGION_CODES", "US,GB,JP,ES").split(",")
    TREND_CATEGORY_ID: str = os.getenv("TREND_CATEGORY_ID", "28")  # 28 = Science & Technology
    TREND_MAX_RESULTS: int = int(os.getenv("TREND_MAX_RESULTS", "8"))

    # --- Payments (Stripe) ---
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    STRIPE_PRICE_ID: str = os.getenv("STRIPE_PRICE_ID", "")  # price_xxx for the $29/mo plan

    # --- Email delivery (Mailgun) ---
    MAILGUN_API_KEY: str = os.getenv("MAILGUN_API_KEY", "")
    MAILGUN_DOMAIN: str = os.getenv("MAILGUN_DOMAIN", "")
    MAILGUN_FROM: str = os.getenv("MAILGUN_FROM", "TrendPulse <newsletter@example.com>")

    # --- App ---
    LP_BASE_URL: str = os.getenv("LP_BASE_URL", "https://your-domain.example.com")
    DB_PATH: str = os.getenv("DB_PATH", "trendpulse.db")
    INTERNAL_TRIGGER_TOKEN: str = os.getenv("INTERNAL_TRIGGER_TOKEN", "")  # protects /internal/* routes
    CORS_ORIGINS: list[str] = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
