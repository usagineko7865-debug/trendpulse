import { useState } from "react";
import PulseLine from "./PulseLine.jsx";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function Hero() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState("idle"); // idle | loading | done | error

  async function handleSubmit(e) {
    e.preventDefault();
    if (!email) return;
    setStatus("loading");
    try {
      const res = await fetch(`${API_BASE}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      if (!res.ok) throw new Error("signup failed");
      setStatus("done");
    } catch {
      setStatus("error");
    }
  }

  return (
    <div className="relative">
      <nav className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-6">
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-coral text-white shadow-pop">
            <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none">
              <path
                d="M3 12h4l2-7 4 14 2-7h6"
                stroke="currentColor"
                strokeWidth="2.2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <span className="font-display text-lg font-semibold tracking-tight text-ink">
            TrendPulse
          </span>
        </div>
        <div className="flex items-center gap-3">
          <a
            href="#pricing"
            className="hidden text-sm font-medium text-ink-soft transition hover:text-ink sm:block"
          >
            Pricing
          </a>
          <a
            href="#signup"
            className="rounded-full bg-ink px-4 py-2 text-sm font-semibold text-paper transition hover:bg-coral-deep"
          >
            Get started
          </a>
        </div>
      </nav>

      <header className="mx-auto grid max-w-6xl gap-14 px-6 pb-20 pt-10 sm:pt-16 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:gap-8">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-coral-soft px-4 py-1.5 text-xs font-semibold text-coral-deep">
            <span className="h-1.5 w-1.5 rounded-full bg-coral" />
            For creators &amp; social teams — never run dry on ideas
          </div>

          <h1 className="mt-6 max-w-xl font-display text-4xl font-semibold leading-[1.08] tracking-tight text-ink sm:text-[3.4rem]">
            The internet's pulse,{" "}
            <span className="text-coral">before your coffee's ready.</span>
          </h1>

          <p className="mt-6 max-w-lg text-balance text-lg leading-relaxed text-ink-soft">
            Stop guessing what to post today. TrendPulse scans real trending
            videos worldwide every morning and hands you the angles worth
            making content about — before your competitors spot them.
          </p>

          <form
            id="signup"
            onSubmit={handleSubmit}
            className="mt-9 flex w-full max-w-md flex-col gap-3 sm:flex-row"
          >
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@email.com"
              className="w-full rounded-full border-2 border-line bg-card px-5 py-3.5 text-sm text-ink placeholder-ink-faint outline-none transition focus:border-coral"
            />
            <button
              type="submit"
              disabled={status === "loading"}
              className="shrink-0 rounded-full bg-coral px-6 py-3.5 text-sm font-semibold text-white shadow-pop transition hover:bg-coral-deep disabled:opacity-60"
            >
              {status === "loading" ? "Joining…" : "Join the free feed"}
            </button>
          </form>

          <p className="mt-3 text-xs text-ink-faint">
            {status === "done"
              ? "You're in! Bookmark this page — fresh trend angles land here every morning. Want it delivered to your inbox instead? Upgrade to Pro anytime. 🎉"
              : status === "error"
              ? "Couldn't reach the API — is the backend running?"
              : "Free web feed · no credit card · email delivery is included with Pro"}
          </p>

          <div className="mt-10 flex flex-wrap items-center gap-x-6 gap-y-3 text-sm text-ink-soft">
            <TrustBadge label="Real trending videos, never invented" />
            <TrustBadge label="EN · ES · JA every day" />
            <TrustBadge label="Fresh angles on the site every morning" />
          </div>
        </div>

        {/* hero visual: a stylised preview of the actual newsletter, not an abstract dashboard */}
        <div className="relative">
          <div className="pointer-events-none absolute -inset-8 -z-10 rounded-[3rem] bg-coral-soft/50 blur-2xl" />
          <div className="rounded-xl2 border border-line bg-card p-2 shadow-lift sm:rotate-1">
            <div className="rounded-[1.4rem] border border-line/70 bg-paper-soft px-5 py-4">
              <div className="flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-full bg-coral" />
                <span className="h-2.5 w-2.5 rounded-full bg-[#F5CD79]" />
                <span className="h-2.5 w-2.5 rounded-full bg-teal" />
                <span className="ml-3 text-xs font-medium text-ink-faint">
                  Today's Pulse — 7:00 AM
                </span>
              </div>
            </div>
            <div className="space-y-4 px-6 py-6">
              <p className="text-xs font-semibold uppercase tracking-wide text-coral">
                Hardware &amp; gadgets
              </p>
              <h3 className="font-display text-xl font-semibold leading-snug text-ink">
                Durability content is having a moment 🔧
              </h3>
              <p className="text-sm leading-relaxed text-ink-soft">
                Three videos this week mine the "will it survive" instinct —
                repair teardown, benchmark stunt, and a phone with a bend
                test. Here's an angle worth filming before it saturates…
              </p>
              <div className="flex flex-wrap gap-2 pt-1">
                <TrendChip color="coral">10.5M views</TrendChip>
                <TrendChip color="teal">7.1% engagement</TrendChip>
                <TrendChip color="ink">🇪🇸 ES source</TrendChip>
              </div>
            </div>
            <div className="flex items-center justify-between border-t border-line px-6 py-4">
              <span className="text-xs text-ink-faint">
                Sent to 1 reader today. Could be more.
              </span>
              <span className="text-xs font-semibold text-teal">
                Delivered by 7am ✓
              </span>
            </div>
          </div>
        </div>
      </header>

      <PulseLine className="h-6 w-full text-line" />
    </div>
  );
}

function TrustBadge({ label }) {
  return (
    <span className="inline-flex items-center gap-1.5">
      <svg viewBox="0 0 20 20" fill="none" className="h-4 w-4 shrink-0 text-teal">
        <path
          d="M4 10l4 4 8-8"
          stroke="currentColor"
          strokeWidth="2.4"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      {label}
    </span>
  );
}

function TrendChip({ children, color }) {
  const styles = {
    coral: "bg-coral-soft text-coral-deep",
    teal: "bg-teal-soft text-teal",
    ink: "bg-paper-soft text-ink-soft",
  };
  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-semibold ${styles[color]}`}
    >
      {children}
    </span>
  );
}
