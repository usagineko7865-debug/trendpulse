const STRIPE_PAYMENT_LINK =
  import.meta.env.VITE_STRIPE_PAYMENT_LINK || "https://buy.stripe.com/REPLACE_WITH_YOUR_LINK";

export default function Pricing() {
  return (
    <section id="pricing" className="mx-auto max-w-6xl px-6 py-20">
      <div className="mx-auto mb-14 max-w-2xl text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-coral">
          Pricing
        </p>
        <h2 className="mt-3 font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
          Simple, honest pricing
        </h2>
        <p className="mt-4 text-ink-soft">
          Start free. Upgrade when the deep-dive angles start saving you
          real research time.
        </p>
      </div>

      <div className="mx-auto grid max-w-3xl gap-6 sm:grid-cols-2">
        {/* Free plan */}
        <div className="rounded-xl2 border border-line bg-card p-8 shadow-card">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-ink-faint">
            Free
          </h3>
          <div className="mt-3 flex items-baseline gap-1">
            <span className="font-display text-4xl font-semibold text-ink">$0</span>
            <span className="text-sm text-ink-faint">/mo</span>
          </div>
          <ul className="mt-6 space-y-3 text-sm text-ink-soft">
            <PlanItem>Daily multilingual trend post (EN/ES/JA)</PlanItem>
            <PlanItem>Top-3 content-worthy videos, twice a week</PlanItem>
            <PlanItem>Community access</PlanItem>
          </ul>
          <a
            href="#signup"
            className="mt-8 block w-full rounded-full border-2 border-line py-3 text-center text-sm font-semibold text-ink transition hover:border-ink"
          >
            Get Started
          </a>
        </div>

        {/* Paid plan */}
        <div className="relative overflow-hidden rounded-xl2 border-2 border-coral bg-card p-8 shadow-pop">
          <div className="absolute right-6 top-6 rounded-full bg-coral px-3 py-1 text-[11px] font-semibold text-white">
            Most Popular
          </div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-coral-deep">
            Pro
          </h3>
          <div className="mt-3 flex items-baseline gap-1">
            <span className="font-display text-4xl font-semibold text-ink">$29</span>
            <span className="text-sm text-ink-faint">/mo</span>
          </div>
          <ul className="mt-6 space-y-3 text-sm text-ink-soft">
            <PlanItem>Full daily deep-dive newsletter</PlanItem>
            <PlanItem>Every trending video, every region — before it peaks</PlanItem>
            <PlanItem>Ready-to-post multilingual social drafts</PlanItem>
            <PlanItem>Cancel anytime</PlanItem>
          </ul>
          {/* Wire STRIPE_PAYMENT_LINK to a real Stripe Payment Link (or
              Checkout Session URL) via the VITE_STRIPE_PAYMENT_LINK env var
              before deploying — this placeholder does not process payment. */}
          <a
            href={STRIPE_PAYMENT_LINK}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-8 block w-full rounded-full bg-coral py-3 text-center text-sm font-semibold text-white transition hover:bg-coral-deep"
          >
            Upgrade to Pro
          </a>
        </div>
      </div>
    </section>
  );
}

function PlanItem({ children }) {
  return (
    <li className="flex items-start gap-2">
      <svg viewBox="0 0 20 20" fill="none" className="mt-0.5 h-4 w-4 shrink-0 text-teal">
        <path
          d="M4 10l4 4 8-8"
          stroke="currentColor"
          strokeWidth="2.4"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      {children}
    </li>
  );
}
