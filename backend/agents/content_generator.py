"""ContentGeneratorAgent — turns a TrendBatch into (1) a long-form paid
newsletter and (2) short multilingual social posts, using the real Anthropic
Messages API (claude-opus-4-8).

Design choices worth knowing:
- The newsletter uses streaming (`client.messages.stream`) because long-form
  output risks HTTP timeouts on a plain request.
- Social posts use `output_config.format` (structured outputs) so the model
  is *constrained* to return valid JSON with exactly the three language
  keys — no regex-parsing a free-text response.
- The LP URL is appended to each post in code, not left to the model, so a
  post can never ship without the link no matter what the model does.
"""
from __future__ import annotations

import json
import logging

import anthropic

from config import get_settings
from agents.trend_scraper import TrendBatch

logger = logging.getLogger("trendpulse.content_generator")

NEWSLETTER_SYSTEM = """You are the lead analyst for TrendPulse, a paid tech/business \
intelligence newsletter. You write for professionals who pay to skip the noise. \
Write with concrete specifics from the data given — real titles, real channels, real \
numbers. Never invent statistics or claims not present in the source data. \
Structure: a 2-3 sentence executive summary, then one section per trend with a \
sharp "why this matters for builders/investors" takeaway. Output clean HTML \
(h2/h3/p/ul only, no <html>/<head>/<body> wrapper) suitable for embedding in an \
email template."""

SOCIAL_SYSTEM = """You write short, high-signal social posts (X and LinkedIn style) \
summarizing a tech trend for a general audience, in three languages: English, \
Spanish, and Japanese. Each post must stand alone (no "as mentioned above"), \
name the concrete trend, and end with a one-line hook — but do NOT include any \
URL or link; the caller appends the link separately. Keep each post under 260 \
characters (excluding the language name) so there is room left for the link."""

SOCIAL_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "en": {"type": "string", "description": "English post, no link"},
        "es": {"type": "string", "description": "Spanish post, no link"},
        "ja": {"type": "string", "description": "Japanese post, no link"},
    },
    "required": ["en", "es", "ja"],
    "additionalProperties": False,
}


class ContentGeneratorAgent:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        settings = get_settings()
        key = api_key or settings.ANTHROPIC_API_KEY
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set.")
        self.client = anthropic.Anthropic(api_key=key)
        self.model = model or settings.ANTHROPIC_MODEL
        self.lp_base_url = settings.LP_BASE_URL

    def _trend_context(self, batch: TrendBatch, limit: int = 8) -> str:
        lines = []
        for item in batch.items[:limit]:
            lines.append(
                f"- \"{item.title}\" by {item.channel} ({item.region}) — "
                f"{item.why_trending}. {item.url}"
            )
        return "\n".join(lines)

    def generate_newsletter(self, batch: TrendBatch) -> str:
        """Long-form paid-tier issue. Streams to avoid request timeouts."""
        context = self._trend_context(batch)
        user_msg = (
            "Today's real trending tech/business videos (source: YouTube Data API, "
            "actual metrics, do not alter):\n\n"
            f"{context}\n\n"
            "Write today's TrendPulse issue."
        )
        with self.client.messages.stream(
            model=self.model,
            max_tokens=4000,
            system=NEWSLETTER_SYSTEM,
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
            messages=[{"role": "user", "content": user_msg}],
        ) as stream:
            message = stream.get_final_message()
        text = "".join(block.text for block in message.content if block.type == "text")
        return text

    def generate_social_posts(self, batch: TrendBatch) -> dict[str, str]:
        """Multilingual acquisition posts, structured-output guaranteed JSON,
        LP link appended deterministically in code (never trust the model
        for the one part of the output that actually drives revenue)."""
        top = batch.items[0] if batch.items else None
        if top is None:
            raise ValueError("Cannot generate social posts from an empty trend batch.")
        user_msg = (
            f"Today's #1 trending video: \"{top.title}\" by {top.channel}. "
            f"{top.why_trending}. Write the three-language post set."
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=SOCIAL_SYSTEM,
            output_config={"format": {"type": "json_schema", "schema": SOCIAL_POST_SCHEMA}},
            messages=[{"role": "user", "content": user_msg}],
        )
        text = next(b.text for b in response.content if b.type == "text")
        posts: dict[str, str] = json.loads(text)

        link = f"{self.lp_base_url}?utm_source=social&utm_medium=auto&utm_campaign=trend"
        return {lang: f"{body}\n\n{link}" for lang, body in posts.items()}
