"""Real Stripe webhook handler with signature verification (via the official
`stripe` Python SDK). This is the trigger that turns a Checkout payment into
a 'pro' subscriber row — never trust an unsigned request here.

Wiring on Stripe's side (one-time setup, done in the Stripe Dashboard, not
in code): create a Payment Link or Checkout Session for the $29/mo Price,
then add a webhook endpoint pointing at POST /webhooks/stripe listening for
at minimum: checkout.session.completed, customer.subscription.updated,
customer.subscription.deleted.
"""
from __future__ import annotations

import logging

import stripe

from config import get_settings
import db

logger = logging.getLogger("trendpulse.stripe_webhook")


class StripeWebhookHandler:
    def __init__(self):
        settings = get_settings()
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def verify_and_parse(self, payload: bytes, sig_header: str) -> stripe.Event:
        """Raises stripe.error.SignatureVerificationError on a forged/invalid
        payload — callers must turn that into an HTTP 400, never a 200."""
        return stripe.Webhook.construct_event(payload, sig_header, self.webhook_secret)

    def handle_event(self, event: stripe.Event) -> None:
        etype = event["type"]
        obj = event["data"]["object"]

        if etype == "checkout.session.completed":
            email = obj.get("customer_details", {}).get("email") or obj.get("customer_email")
            customer_id = obj.get("customer")
            subscription_id = obj.get("subscription")
            if email:
                db.upsert_subscriber_from_stripe(
                    email=email,
                    stripe_customer_id=customer_id,
                    stripe_subscription_id=subscription_id,
                    plan="pro",
                    status="active",
                )
                logger.info("Stripe: activated pro subscriber %s", email)

        elif etype == "customer.subscription.updated":
            status = obj.get("status")  # active | past_due | canceled | ...
            customer_id = obj.get("customer")
            self._update_status_by_customer(customer_id, status)

        elif etype == "customer.subscription.deleted":
            customer_id = obj.get("customer")
            self._update_status_by_customer(customer_id, "canceled")

        else:
            logger.debug("Stripe: unhandled event type %s", etype)

    def _update_status_by_customer(self, customer_id: str | None, status: str) -> None:
        if not customer_id:
            return
        # Minimal direct update; a production system would look up the row by
        # stripe_customer_id first. Kept explicit here for readability.
        with db.get_conn() as conn:
            conn.execute(
                "UPDATE subscribers SET status = ?, updated_at = strftime('%s','now') "
                "WHERE stripe_customer_id = ?",
                (status, customer_id),
            )
        logger.info("Stripe: customer %s subscription status -> %s", customer_id, status)
