"""FastAPI application entry point. Run with:

    uvicorn main:app --reload --port 8000

Routes:
    GET  /                       health check
    POST /signup                 free web-feed signup (adds a 'free' subscriber)
    POST /webhooks/stripe        Stripe webhook (checkout/subscription lifecycle)
    POST /internal/run-cycle     manually trigger the AutomationWorkflow (protected)
    GET  /internal/latest-issue  inspect the most recently generated issue (protected)
    GET  /internal/stats         aggregate subscriber/issue counts, no PII (protected)
    POST /internal/test-email    send one test email to a given address (protected)

Scheduling: this file does NOT run a built-in scheduler by design (keeps the
web process lightweight and horizontally scalable). Point any external
scheduler — a host cron job, a platform's scheduled-job feature, or
APScheduler if you prefer an in-process option — at POST /internal/run-cycle
with the INTERNAL_TRIGGER_TOKEN header once a day.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import stripe

from config import get_settings
import db
from stripe_webhook import StripeWebhookHandler
from workflow.automation import AutomationWorkflow
from email_service import EmailService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trendpulse.main")

settings = get_settings()

app = FastAPI(title="TrendPulse API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    db.init_db()
    logger.info("TrendPulse API started. DB ready at %s", settings.DB_PATH)


class SignupRequest(BaseModel):
    email: EmailStr


@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": "trendpulse"}


@app.post("/signup")
def signup(body: SignupRequest) -> dict:
    """Free-trial capture from the LP's 'Start Free Trial' form."""
    db.add_free_subscriber(body.email)
    return {"status": "ok", "email": body.email, "plan": "free"}


@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request, stripe_signature: str | None = Header(None)):
    """Real signature-verified Stripe webhook. Returns 400 on any signature
    or parsing failure — Stripe will retry, which is the correct behavior
    for a transient failure, and the correct behavior for a forged request
    is simply to never be trusted in the first place."""
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

    payload = await request.body()
    handler = StripeWebhookHandler()
    try:
        event = handler.verify_and_parse(payload, stripe_signature)
    except stripe.error.SignatureVerificationError as exc:
        logger.warning("Stripe webhook signature verification failed: %s", exc)
        raise HTTPException(status_code=400, detail="Invalid signature") from exc
    except Exception as exc:  # noqa: BLE001
        logger.error("Stripe webhook parse error: %s", exc)
        raise HTTPException(status_code=400, detail="Malformed payload") from exc

    handler.handle_event(event)
    return {"received": True}


def _check_internal_token(token: str | None) -> None:
    if not settings.INTERNAL_TRIGGER_TOKEN:
        # No token configured — refuse to run rather than silently allowing
        # an unauthenticated trigger in a misconfigured deployment.
        raise HTTPException(
            status_code=503,
            detail="INTERNAL_TRIGGER_TOKEN is not configured on the server.",
        )
    if token != settings.INTERNAL_TRIGGER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing internal trigger token")


@app.post("/internal/run-cycle")
async def run_cycle(request: Request, x_internal_token: str | None = Header(None)):
    """Manually (or externally-scheduler-)trigger one full
    scrape -> generate -> deliver cycle. Protect this route — anyone who can
    call it can trigger a paid-subscriber email blast."""
    _check_internal_token(x_internal_token)
    body: dict = {}
    try:
        body = await request.json()
    except Exception:  # noqa: BLE001 — empty body is fine
        pass
    workflow = AutomationWorkflow()
    result = await workflow.run_from_webhook(body)
    return result


@app.get("/internal/latest-issue")
def latest_issue(x_internal_token: str | None = Header(None)):
    _check_internal_token(x_internal_token)
    row = db.latest_issue()
    if row is None:
        raise HTTPException(status_code=404, detail="No issues generated yet")
    return dict(row)


@app.get("/internal/stats")
def stats(x_internal_token: str | None = Header(None)):
    """Aggregate counts only (no emails) — cheap way to check real growth
    without needing direct DB/SSH access to the deployed container."""
    _check_internal_token(x_internal_token)
    return db.subscriber_stats()


class TestEmailRequest(BaseModel):
    to: EmailStr


@app.post("/internal/test-email")
async def test_email(body: TestEmailRequest, x_internal_token: str | None = Header(None)):
    """Sends one real test email through whatever EmailService is currently
    configured — added to verify delivery end-to-end after replacing
    sandbox-locked Mailgun, without needing to fake a subscriber into 'pro'
    status just to trigger a send. Kept around since we've changed email
    providers twice already and this is the fastest way to confirm the next
    one actually works too."""
    _check_internal_token(x_internal_token)
    emailer = EmailService()
    ok = await emailer.send(
        body.to,
        "TrendPulse — test email",
        "<p>This is a test email from TrendPulse's backend, confirming email delivery works.</p>",
    )
    if not ok:
        raise HTTPException(status_code=502, detail="Send failed — check server logs")
    return {"status": "ok", "to": body.to}
