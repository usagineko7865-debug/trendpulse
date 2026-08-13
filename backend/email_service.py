"""Real Mailgun REST API sender (not a mock). Mailgun's HTTP API needs only
an API key + verified domain — no SMTP server to run. Free tier / low volume
is inexpensive, which matters since this fires per-subscriber per issue.
"""
from __future__ import annotations

import asyncio
import logging

import httpx

from config import get_settings

logger = logging.getLogger("trendpulse.email_service")


class EmailService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.MAILGUN_API_KEY
        self.domain = settings.MAILGUN_DOMAIN
        self.from_addr = settings.MAILGUN_FROM
        self.endpoint = f"https://api.mailgun.net/v3/{self.domain}/messages"

    async def send(self, to: str, subject: str, html: str) -> bool:
        if not self.api_key or not self.domain:
            logger.warning("MAILGUN_API_KEY/MAILGUN_DOMAIN not set — skipping send to %s", to)
            return False
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    self.endpoint,
                    auth=("api", self.api_key),
                    data={"from": self.from_addr, "to": to, "subject": subject, "html": html},
                    timeout=15.0,
                )
                resp.raise_for_status()
                return True
            except httpx.HTTPStatusError as exc:
                logger.error("Mailgun send failed for %s: %s — %s", to, exc, exc.response.text)
                return False
            except httpx.RequestError as exc:
                logger.error("Mailgun request error for %s: %s", to, exc)
                return False

    async def send_bulk(self, recipients: list[str], subject: str, html: str,
                         concurrency: int = 10) -> dict[str, int]:
        """Fan out sends with bounded concurrency so we don't hammer Mailgun's
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
