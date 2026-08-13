"""TrendScraperAgent — pulls REAL trending video data. No LLM hallucination.

Why this matters: a "trend newsletter" that quietly has an LLM invent
plausible-sounding trending videos would be selling fabricated data to
paying subscribers. This agent instead calls the YouTube Data API v3
`videos?chart=mostPopular` endpoint per region, which returns actual current
trending videos with real titles, channel names, view counts and URLs.

Get a free key: https://console.cloud.google.com/apis/credentials
(enable "YouTube Data API v3" on the project first). Free quota (10,000
units/day) comfortably covers a few runs per day for several regions.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

import httpx

from config import get_settings

logger = logging.getLogger("trendpulse.trend_scraper")

YOUTUBE_VIDEOS_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"


@dataclass
class TrendItem:
    title: str
    channel: str
    url: str
    view_count: int
    region: str
    published_at: str
    why_trending: str  # heuristic explanation derived from real metrics, not invented


@dataclass
class TrendBatch:
    items: list[TrendItem] = field(default_factory=list)

    def as_dicts(self) -> list[dict]:
        return [item.__dict__ for item in self.items]


class TrendScraperAgent:
    """Fetches real trending tech/business videos per region via YouTube Data API v3."""

    def __init__(self, api_key: str | None = None, timeout: float = 15.0):
        settings = get_settings()
        self.api_key = api_key or settings.YOUTUBE_API_KEY
        self.category_id = settings.TREND_CATEGORY_ID
        self.max_results = settings.TREND_MAX_RESULTS
        self.regions = settings.TREND_REGION_CODES
        self.timeout = timeout

    def _why_trending(self, view_count: int, like_count: int, comment_count: int) -> str:
        """Deterministic, metric-derived explanation — not an invented narrative."""
        engagement = (like_count + comment_count) / max(view_count, 1)
        if engagement > 0.05:
            return f"{view_count:,} views with unusually high engagement ({engagement:.1%} likes+comments/view)"
        if view_count > 1_000_000:
            return f"{view_count:,} views — broad mainstream reach"
        return f"{view_count:,} views, rising fast in its region's trending chart"

    async def fetch_region(self, client: httpx.AsyncClient, region: str) -> list[TrendItem]:
        if not self.api_key:
            raise RuntimeError(
                "YOUTUBE_API_KEY is not set. Get a free key from "
                "https://console.cloud.google.com/apis/credentials and set it "
                "as an environment variable before running the scraper."
            )
        params = {
            "part": "snippet,statistics",
            "chart": "mostPopular",
            "regionCode": region,
            "videoCategoryId": self.category_id,
            "maxResults": self.max_results,
            "key": self.api_key,
        }
        resp = await client.get(YOUTUBE_VIDEOS_ENDPOINT, params=params, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()

        items: list[TrendItem] = []
        for v in data.get("items", []):
            snippet = v["snippet"]
            stats = v.get("statistics", {})
            view_count = int(stats.get("viewCount", 0))
            like_count = int(stats.get("likeCount", 0))
            comment_count = int(stats.get("commentCount", 0))
            items.append(
                TrendItem(
                    title=snippet["title"],
                    channel=snippet["channelTitle"],
                    url=f"https://www.youtube.com/watch?v={v['id']}",
                    view_count=view_count,
                    region=region,
                    published_at=snippet["publishedAt"],
                    why_trending=self._why_trending(view_count, like_count, comment_count),
                )
            )
        return items

    async def run(self) -> TrendBatch:
        """Fetch trending videos across all configured regions, deduplicated by URL."""
        batch = TrendBatch()
        seen_urls: set[str] = set()
        async with httpx.AsyncClient() as client:
            for region in self.regions:
                try:
                    region_items = await self.fetch_region(client, region.strip())
                except Exception as exc:  # noqa: BLE001 — one bad region shouldn't kill the run
                    logger.warning("trend fetch failed for region=%s: %s", region, exc)
                    continue
                for item in region_items:
                    if item.url not in seen_urls:
                        seen_urls.add(item.url)
                        batch.items.append(item)
        batch.items.sort(key=lambda i: i.view_count, reverse=True)
        logger.info("TrendScraperAgent: collected %d unique trending videos", len(batch.items))
        return batch
