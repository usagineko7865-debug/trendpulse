"""Sends real email via Gmail SMTP (not a mock) using an App Password —
not Mailgun. Mailgun's free tier only gives a "sandbox" domain, which is
hard-restricted to a handful of pre-authorized recipient addresses; a real
subscriber would never receive anything. Gmail SMTP needs no domain
verification and just works, at the cost of Gmail's own send limits
(~500/day on a plain account) — fine for this project's current scale.

smtplib is blocking, so every send runs in a worker thread via
asyncio.to_thread to keep this awaitable without blocking the event loop.
"""
from __future__ import annotations

import asyncio
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from config import get_settings

logger = logging.getLogger("trendpulse.email_service")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587  # STARTTLS


class EmailService:
    def __init__(self):
        settings = get_settings()
        self.address = settings.GMAIL_ADDRESS
        self.app_password = settings.GMAIL_APP_PASSWORD
        self.from_name = settings.MAIL_FROM_NAME

    def _send_sync(self, to: str, subject: str, html: str) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = formataddr((self.from_name, self.address))
        msg["To"] = to
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(self.address, self.app_password)
            smtp.sendmail(self.address, [to], msg.as_string())

    async def send(self, to: str, subject: str, html: str) -> bool:
        if not self.address or not self.app_password:
            logger.warning("GMAIL_ADDRESS/GMAIL_APP_PASSWORD not set — skipping send to %s", to)
            return False
        try:
            await asyncio.to_thread(self._send_sync, to, subject, html)
            return True
        except smtplib.SMTPException as exc:
            logger.error("Gmail SMTP send failed for %s: %s", to, exc)
            return False
        except OSError as exc:
            logger.error("Gmail SMTP connection error for %s: %s", to, exc)
            return False

    async def send_bulk(self, recipients: list[str], subject: str, html: str,
                         concurrency: int = 5) -> dict[str, int]:
        """Fan out sends with bounded concurrency. Kept low (5) relative to
        the old Mailgun version's 10 — Gmail is more sensitive to bursts of
        simultaneous SMTP connections than an HTTP API is."""
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
