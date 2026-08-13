"""AutomationWorkflow — the main control task the user asked for: it wires
TrendScraperAgent -> ContentGeneratorAgent -> DB -> EmailService into one
run, and exposes both a schedule-friendly entry point and a
webhook/API-triggerable one. No human ever touches an issue before it goes
out — this *is* the "no human in the loop" pipeline.
"""
from __future__ import annotations

import json
import logging

import db
from agents.trend_scraper import TrendScraperAgent
from agents.content_generator import ContentGeneratorAgent
from email_service import EmailService

logger = logging.getLogger("trendpulse.automation")


class AutomationWorkflow:
    """Orchestrates one full trend -> content -> delivery cycle.

    Usage:
        workflow = AutomationWorkflow()
        result = await workflow.run_daily_cycle()

    Safe to call repeatedly (e.g. from a cron trigger or APScheduler job) —
    each call produces a new `issues` row; nothing is mutated in place.
    """

    def __init__(self):
        self.scraper = TrendScraperAgent()
        self.generator = ContentGeneratorAgent()
        self.emailer = EmailService()

    async def run_daily_cycle(self, send_email: bool = True) -> dict:
        logger.info("AutomationWorkflow: starting daily cycle")

        # 1. Collect real trend data (no LLM invention — see trend_scraper.py).
        batch = await self.scraper.run()
        if not batch.items:
            logger.warning("AutomationWorkflow: no trend items collected, aborting cycle")
            return {"status": "skipped", "reason": "no_trend_data"}

        # 2. Generate the paid newsletter + multilingual acquisition posts.
        newsletter_html = self.generator.generate_newsletter(batch)
        social_posts = self.generator.generate_social_posts(batch)

        # 3. Persist the issue (audit trail + lets /internal endpoints inspect
        #    the latest output without re-running the pipeline).
        issue_id = db.save_issue(
            trend_json=json.dumps(batch.as_dicts(), ensure_ascii=False),
            newsletter_html=newsletter_html,
            social_posts_json=json.dumps(social_posts, ensure_ascii=False),
        )
        logger.info("AutomationWorkflow: saved issue #%d", issue_id)

        result = {
            "status": "ok",
            "issue_id": issue_id,
            "trend_count": len(batch.items),
            "social_posts": social_posts,
            "email": None,
        }

        # 4. Deliver to paying ('pro') subscribers only — free tier gets the
        #    social posts/LP, not the deep-dive newsletter.
        if send_email:
            recipients = [s.email for s in db.list_active_subscribers(plan="pro")]
            if recipients:
                subject = f"TrendPulse — Today's Top {len(batch.items)} Tech/Business Trends"
                stats = await self.emailer.send_bulk(recipients, subject, newsletter_html)
                db.mark_issue_sent(issue_id)
                result["email"] = stats
                logger.info("AutomationWorkflow: emailed %d/%d pro subscribers",
                            stats["sent"], len(recipients))
            else:
                logger.info("AutomationWorkflow: no active pro subscribers to email")
                result["email"] = {"sent": 0, "failed": 0}

        return result

    async def run_from_webhook(self, payload: dict | None = None) -> dict:
        """Entry point for an API-webhook trigger (e.g. an external scheduler
        hitting POST /internal/run-cycle). `payload` is accepted for future
        extensibility (e.g. forcing send_email=False for a dry run) but the
        default behavior ignores it and runs the full cycle."""
        send_email = True
        if payload and isinstance(payload, dict):
            send_email = bool(payload.get("send_email", True))
        return await self.run_daily_cycle(send_email=send_email)
