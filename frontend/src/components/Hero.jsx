import { useState } from "react";

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
    <header className="relative mx-auto flex max-w-6xl flex-col items-center px-6 pb-24 pt-28 text-center sm:pt-36">
      <nav className="absolute left-0 right-0 top-0 mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-6">
        <div className="flex items-center gap-2">
          <div className="h-7 w-7 rounded-md bg-cta-gradient shadow-glow" />
          <span className="text-lg font-bold tracking-tight text-white">TrendPulse</span>
        </div>
        <a
          href="#pricing"
          className="rounded-full border border-white/10 px-4 py-2 text-sm font-medium text-slate-300 transition hover:border-white/30 hover:text-white"
        >
          Pricing
        </a>
      </nav>

      <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-neon-purple/30 bg-neon-purple/10 px-4 py-1.5 text-xs font-medium text-neon-purple">
        <span className="h-1.5 w-1.5 animate-pulse-slow rounded-full bg-neon-purple" />
        Fully autonomous — zero human editors
      </div>

      <h1 className="max-w-3xl text-4xl font-extrabold leading-[1.1] tracking-tight text-white sm:text-6xl">
        Monetize Global Trends,{" "}
        <span className="text-gradient">Automatically.</span>
      </h1>

      <p className="mt-6 max-w-xl text-balance text-lg text-slate-400">
        TrendPulse scrapes real trending videos worldwide, turns them into a
        multilingual newsletter and viral social posts, and delivers it all —
        with no human in the loop.
      </p>

      <form
        onSubmit={handleSubmit}
        className="mt-10 flex w-full max-w-md flex-col gap-3 sm:flex-row"
      >
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@company.com"
          className="w-full rounded-full border border-white/10 bg-white/5 px-5 py-3 text-sm text-white placeholder-slate-500 outline-none transition focus:border-neon-purple/60 focus:ring-2 focus:ring-neon-purple/20"
        />
        <button
          type="submit"
          disabled={status === "loading"}
          className="group relative shrink-0 overflow-hidden rounded-full bg-cta-gradient px-6 py-3 text-sm font-semibold text-white shadow-glow transition hover:shadow-glow-blue disabled:opacity-60"
        >
          {status === "loading" ? "Starting…" : "Start Free Trial"}
        </button>
      </form>

      <p className="mt-3 text-xs text-slate-500">
        {status === "done"
          ? "You're in! Check your inbox for your first free issue."
          : status === "error"
          ? "Couldn't reach the API — is the backend running?"
          : "No credit card required. Cancel anytime."}
      </p>
    </header>
  );
}
