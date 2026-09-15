const FEATURES = [
  {
    step: "01",
    title: "Scrapes real trends",
    tone: "coral",
    description:
      "Pulls real-time trending tech & business videos worldwide via the YouTube Data API — actual titles, channels, and view metrics, never invented data.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6">
        <path
          d="M3 17l6-6 4 4 8-8M21 7v6M21 7h-6"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    step: "02",
    title: "Writes it up, warmly",
    tone: "teal",
    description:
      "Claude drafts a deep-dive newsletter for paying subscribers, plus punchy social posts in English, Spanish, and Japanese — never the same sentence twice.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6">
        <path
          d="M4 5h9M4 5c0 6 3 9 9 9M9 5c0 8 5 12 10 12M15 12h6l-3-6-3 6zM15 21l1.5-3M19.5 18l1.5 3"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    step: "03",
    title: "Ships itself",
    tone: "coral",
    description:
      "A Stripe payment instantly activates new subscribers; a scheduled workflow sends each issue straight to their inbox via Mailgun — nobody clicks send.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-6 w-6">
        <path
          d="M3 8l9 6 9-6M4 6h16a1 1 0 011 1v10a1 1 0 01-1 1H4a1 1 0 01-1-1V7a1 1 0 011-1z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
];

const TONE = {
  coral: "bg-coral-soft text-coral-deep",
  teal: "bg-teal-soft text-teal",
};

export default function Features() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-20">
      <div className="mx-auto mb-14 max-w-2xl text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-coral">
          How you get your next idea
        </p>
        <h2 className="mt-3 font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
          One pipeline. Zero humans. Zero guesswork.
        </h2>
        <p className="mt-4 text-ink-soft">
          Three steps, every single day — from raw trend data to a content
          idea ready to use, with nobody in between.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-3">
        {FEATURES.map((f) => (
          <div
            key={f.title}
            className="group relative rounded-xl2 border border-line bg-card p-7 shadow-card transition hover:-translate-y-1"
          >
            <span className="absolute right-6 top-6 font-display text-3xl font-semibold text-paper-soft">
              {f.step}
            </span>
            <div
              className={`mb-5 inline-flex h-12 w-12 items-center justify-center rounded-2xl ${TONE[f.tone]}`}
            >
              {f.icon}
            </div>
            <h3 className="mb-2 font-display text-lg font-semibold text-ink">
              {f.title}
            </h3>
            <p className="text-sm leading-relaxed text-ink-soft">
              {f.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
