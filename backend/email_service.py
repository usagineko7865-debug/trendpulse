"""Sends real email via Brevo's transactional email REST API (HTTPS, not
SMTP). Two things were tried and abandoned before this — see config.py's
comment on BREVO_API_KEY for the full chronology — but the short version:
Mailgun's free tier can't actually reach real subscribers (sandbox-only),
and Gmail SMTP is blocked outright by Railway's network regardless of
credentials. Brevo's API is a plain HTTPS POST, same as every other
integration in this app (YouTube/Anthropic/Stripe), so it isn't subject to
whatever is blocking raw SMTP ports there.
"""
from __future__ import annotations

import asyncio
import logging

import httpx

from config import get_settings

logger = logging.getLogger("trendpulse.email_service")

BREVO_ENDPOINT = "https://api.brevo.com/v3/smtp/email"


class EmailService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.BREVO_API_KEY
        self.sender_email = settings.BREVO_SENDER_EMAIL
        self.from_name = settings.MAIL_FROM_NAME

    async def send(self, to: str, subject: str, html: str) -> bool:
        if not self.api_key or not self.sender_email:
            logger.warning("BREVO_API_KEY/BREVO_SENDER_EMAIL not set — skipping send to %s", to)
            return False
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    BREVO_ENDPOINT,
                    headers={
                        "api-key": self.api_key,
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    json={
                        "sender": {"name": self.from_name, "email": self.sender_email},
                        "to": [{"email": to}],
                        "subject": subject,
                        "htmlContent": html,
                    },
                    timeout=15.0,
                )
                resp.raise_for_status()
                return True
            except httpx.HTTPStatusError as exc:
                logger.error("Brevo send failed for %s: %s — %s", to, exc, exc.response.text)
                return False
            except httpx.RequestError as exc:
                logger.error("Brevo request error for %s: %s", to, exc)
                return False

    async def send_bulk(self, recipients: list[str], subject: str, html: str,
                         concurrency: int = 10) -> dict[str, int]:
        """Fan out sends with bounded concurrency so we don't hammer Brevo's
        rate limits on a large subscriber list."""
        sem = asyncio.Semaphore(concurrency)
        sent, failed = 0, 0

        async def _one(addr: str):
            nonlocal sent, failed
            async with sem:
                ok = await self.send(addr, subject, html)
                if ok:
                    sent += 1
                else:
                    failed += 1

        await asyncio.gather(*(_one(r) for r in recipients))
        return {"sent": sent, "failed": failed}
