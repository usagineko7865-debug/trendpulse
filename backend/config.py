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

    # --- Email delivery (Brevo HTTP API) ---
    # Chronology (all 2026-09-16): Mailgun's free tier is sandbox-only
    # (delivers only to a handful of pre-authorized addresses — a real
    # subscriber would never get their newsletter) -> switched to Gmail SMTP
    # with an App Password (free, no domain) -> that failed too, but not on
    # credentials: Railway's containers block outbound SMTP-port traffic
    # entirely (confirmed by sending successfully from a local machine with
    # the exact same credentials, and by every other outbound HTTPS call in
    # this app — YouTube/Anthropic/Stripe — working fine). So the fix isn't
    # "better SMTP code", it's "don't use SMTP" -> Brevo's REST API over
    # HTTPS, which isn't subject to that port block. Free tier: 300
    # emails/day, and verifying one sender address is enough — no owned
    # domain required, unlike Mailgun's paid/verified tier.
    BREVO_API_KEY: str = os.getenv("BREVO_API_KEY", "")
    BREVO_SENDER_EMAIL: str = os.getenv("BREVO_SENDER_EMAIL", "")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "TrendPulse")

    # --- App ---
    LP_BASE_URL: str = os.getenv("LP_BASE_URL", "https://your-domain.example.com")
    DB_PATH: str = os.getenv("DB_PATH", "trendpulse.db")
    INTERNAL_TRIGGER_TOKEN: str = os.getenv("INTERNAL_TRIGGER_TOKEN", "")  # protects /internal/* routes
    CORS_ORIGINS: list[str] = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
