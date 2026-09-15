"""Lightweight persistence layer. SQLite by default (zero-ops, file-based) —
swap the connection string in production for Postgres without touching
callers, since every query goes through these typed helper functions.
"""
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass

from config import get_settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    stripe_customer_id TEXT,
    stripe_subscription_id TEXT,
    plan TEXT NOT NULL DEFAULT 'free',      -- 'free' | 'pro'
    status TEXT NOT NULL DEFAULT 'active',  -- 'active' | 'canceled' | 'past_due'
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at REAL NOT NULL,
    trend_json TEXT NOT NULL,       -- raw scraped trend data, for audit/debug
    newsletter_html TEXT NOT NULL,  -- paid-tier long-form issue
    social_posts_json TEXT NOT NULL,-- {"en": "...", "es": "...", "ja": "..."}
    sent_at REAL
);

CREATE INDEX IF NOT EXISTS idx_subscribers_plan_status ON subscribers(plan, status);
"""


@contextmanager
def get_conn():
    settings = get_settings()
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)


@dataclass
class Subscriber:
    id: int
    email: str
    plan: str
    status: str
    stripe_customer_id: str | None
    stripe_subscription_id: str | None


def upsert_subscriber_from_stripe(
    email: str,
    stripe_customer_id: str,
    stripe_subscription_id: str | None,
    plan: str,
    status: str,
) -> None:
    now = time.time()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO subscribers (email, stripe_customer_id, stripe_subscription_id,
                                      plan, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                stripe_customer_id = excluded.stripe_customer_id,
                stripe_subscription_id = excluded.stripe_subscription_id,
                plan = excluded.plan,
                status = excluded.status,
                updated_at = excluded.updated_at
            """,
            (email, stripe_customer_id, stripe_subscription_id, plan, status, now, now),
        )


def add_free_subscriber(email: str) -> None:
    now = time.time()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO subscribers (email, plan, status, created_at, updated_at)
            VALUES (?, 'free', 'active', ?, ?)
            ON CONFLICT(email) DO NOTHING
            """,
            (email, now, now),
        )


def subscriber_stats() -> dict:
    """Aggregate counts only — no emails/PII — for a cheap internal health check."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT plan, status, COUNT(*) AS n FROM subscribers GROUP BY plan, status"
        ).fetchall()
        total_issues = conn.execute("SELECT COUNT(*) AS n FROM issues").fetchone()["n"]
        latest = conn.execute(
            "SELECT MAX(created_at) AS ts FROM subscribers"
        ).fetchone()["ts"]
    by_plan_status = {f"{r['plan']}_{r['status']}": r["n"] for r in rows}
    return {
        "by_plan_status": by_plan_status,
        "total_subscribers": sum(by_plan_status.values()),
        "total_issues": total_issues,
        "last_signup_at": latest,
    }


def list_active_subscribers(plan: str | None = None) -> list[Subscriber]:
    q = "SELECT * FROM subscribers WHERE status = 'active'"
    args: tuple = ()
    if plan:
        q += " AND plan = ?"
        args = (plan,)
    with get_conn() as conn:
        rows = conn.execute(q, args).fetchall()
    return [
        Subscriber(
            id=r["id"], email=r["email"], plan=r["plan"], status=r["status"],
            stripe_customer_id=r["stripe_customer_id"],
            stripe_subscription_id=r["stripe_subscription_id"],
        )
        for r in rows
    ]


def save_issue(trend_json: str, newsletter_html: str, social_posts_json: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO issues (created_at, trend_json, newsletter_html, social_posts_json)
            VALUES (?, ?, ?, ?)
            """,
            (time.time(), trend_json, newsletter_html, social_posts_json),
        )
        return cur.lastrowid


def mark_issue_sent(issue_id: int) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE issues SET sent_at = ? WHERE id = ?", (time.time(), issue_id))


def latest_issue() -> sqlite3.Row | None:
    with get_conn() as conn:
        return conn.execute("SELECT * FROM issues ORDER BY id DESC LIMIT 1").fetchone()
