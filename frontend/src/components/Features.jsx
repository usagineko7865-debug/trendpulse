const FEATURES = [
  {
    title: "Trend Scraping",
    accent: "text-neon-purple",
    ring: "ring-neon-purple/30",
    description:
      "Pulls real-time trending tech & business videos worldwide via the YouTube Data API — actual titles, channels, and view metrics, never invented data.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6">
        <path
          d="M3 17l6-6 4 4 8-8M21 7v6M21 7h-6"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    title: "Multilingual Copywriting",
    accent: "text-electric-blue",
    ring: "ring-electric-blue/30",
    description:
      "Claude generates a deep-dive English newsletter for paying subscribers, plus punchy English, Spanish, and Japanese social posts for acquisition.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6">
        <path
          d="M4 5h9M4 5c0 6 3 9 9 9M9 5c0 8 5 12 10 12M15 12h6l-3-6-3 6zM15 21l1.5-3M19.5 18l1.5 3"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    title: "Auto-Delivery",
    accent: "text-neon-purple",
    ring: "ring-neon-purple/30",
    description:
      "Stripe payment events trigger instant subscriber activation; a scheduled workflow ships each issue straight to paying inboxes via Mailgun — no manual send.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6">
        <path
          d="M3 8l9 6 9-6M4 6h16a1 1 0 011 1v10a1 1 0 01-1 1H4a1 1 0 01-1-1V7a1 1 0 011-1z"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
];

export default function Features() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-20">
      <div className="mx-auto mb-14 max-w-2xl text-center">
        <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
          One pipeline. Zero humans.
        </h2>
        <p className="mt-4 text-slate-400">
          Three autonomous agents run end-to-end, from raw trend data to a
          paying subscriber's inbox.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-3">
        {FEATURES.map((f) => (
          <div
            key={f.title}
            className="group rounded-2xl border border-white/10 bg-white/[0.03] p-7 transition hover:-translate-y-1 hover:border-white/20 hover:bg-white/[0.05]"
          >
            <div
              className={`mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-white/5 ring-1 ${f.ring} ${f.accent}`}
            >
              {f.icon}
            </div>
            <h3 className="mb-2 text-lg font-semibold text-white">{f.title}</h3>
            <p className="text-sm leading-relaxed text-slate-400">
              {f.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
