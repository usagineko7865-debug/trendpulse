"""Posts today's TrendPulse issue to X (Twitter) via the official API — no browser automation.

Why this exists: the previous approach (a Claude Code scheduled task driving a
browser) was fragile in two independent ways: (1) the browser session's saved
X login cookies could silently expire, and (2) the scheduled-task execution
environment itself would occasionally hang after a file-write and never
recover until a human noticed. Posting via the real X API from a plain
GitHub Actions job sidesteps both failure modes — the same daily-trigger.yml
workflow in this repo has run every day for weeks without a single failure.

Requires four GitHub Actions repo secrets (Settings -> Secrets and variables
-> Actions), all obtained from https://developer.x.com (a Free-tier
Project/App with Read+Write permissions is enough for this):
    X_API_KEY
    X_API_SECRET
    X_ACCESS_TOKEN
    X_ACCESS_TOKEN_SECRET
...plus the two secrets the existing daily-trigger.yml already uses:
    TRENDPULSE_API_URL
    TRENDPULSE_INTERNAL_TOKEN

State (which issue id was last posted) is kept in x_last_posted_issue.txt at
the repo root and committed back by the workflow after a successful post —
this makes the dedup check work across ephemeral GitHub Actions runners
without needing an external database.
"""

import os
import re
import sys
import json
from pathlib import Path

import httpx
import tweepy

# X shortens every http(s) URL to a fixed-width t.co link for length-counting
# purposes, regardless of the URL's real length — a naive len(str) check
# wildly over-counts any tweet with a long tracked link (e.g. one with UTM
# params) and would truncate text that actually fits fine. See
# https://developer.x.com/en/docs/counting-characters
_URL_RE = re.compile(r"https?://\S+")
_TCO_LENGTH = 23


def x_weighted_length(text: str) -> int:
    urls = _URL_RE.findall(text)
    stripped = _URL_RE.sub("", text)
    return len(stripped) + len(urls) * _TCO_LENGTH

STATE_FILE = Path(__file__).resolve().parent.parent / "x_last_posted_issue.txt"

# Simple rotation of evergreen tags. No trend-detection here on purpose —
# this script optimizes for "never hangs, never silently stops", not for the
# extra polish the browser-based task could do. Kept short and unopinionated.
HASHTAGS = ["#buildinpublic", "#indiehackers", "#SaaS", "#contentcreator"]


def get_latest_issue(api_url: str, token: str) -> dict:
    resp = httpx.get(
        f"{api_url}/internal/latest-issue",
        headers={"X-Internal-Token": token},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def already_posted(issue_id) -> bool:
    if not STATE_FILE.exists():
        return False
    return STATE_FILE.read_text().strip() == str(issue_id)


def mark_posted(issue_id) -> None:
    STATE_FILE.write_text(str(issue_id))


def pick_hashtag(issue_id) -> str:
    # Deterministic rotation keyed off the issue id so it varies day to day
    # without needing any extra state.
    return HASHTAGS[int(issue_id) % len(HASHTAGS)]


def build_tweet_text(issue: dict) -> str:
    social_posts = json.loads(issue["social_posts_json"])
    text = social_posts["en"].strip()
    tag = pick_hashtag(issue["id"])
    candidate = f"{text}\n\n{tag}"
    if x_weighted_length(candidate) <= 280:
        return candidate
    # The pipeline's text already contains a real tracked link — never trim
    # it blindly, that risks truncating the URL itself. If it doesn't fit
    # with a hashtag (using X's real, t.co-weighted length), just drop the
    # hashtag. If it *still* doesn't fit, post it as-is and let the API
    # reject it loudly rather than silently mangling a link.
    return text


def main() -> int:
    api_url = os.environ["TRENDPULSE_API_URL"]
    internal_token = os.environ["TRENDPULSE_INTERNAL_TOKEN"]

    issue = get_latest_issue(api_url, internal_token)
    issue_id = issue["id"]

    if already_posted(issue_id):
        print(f"Issue {issue_id} was already posted. Nothing to do.")
        return 0

    tweet_text = build_tweet_text(issue)

    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    response = client.create_tweet(text=tweet_text)
    print(f"Posted tweet id {response.data['id']} for issue {issue_id}:")
    print(tweet_text)

    mark_posted(issue_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
