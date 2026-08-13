const STRIPE_PAYMENT_LINK =
  import.meta.env.VITE_STRIPE_PAYMENT_LINK || "https://buy.stripe.com/REPLACE_WITH_YOUR_LINK";

export default function Pricing() {
  return (
    <section id="pricing" className="mx-auto max-w-6xl px-6 py-20">
      <div className="mx-auto mb-14 max-w-2xl text-center">
        <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
          Simple, honest pricing
        </h2>
        <p className="mt-4 text-slate-400">
          Start free. Upgrade when the deep-dive issues are worth it.
        </p>
      </div>

      <div className="mx-auto grid max-w-3xl gap-6 sm:grid-cols-2">
        {/* Free plan */}
        <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-8">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">
            Free
          </h3>
          <div className="mt-3 flex items-baseline gap-1">
            <span className="text-4xl font-extrabold text-white">$0</span>
            <span className="text-sm text-slate-500">/mo</span>
          </div>
          <ul className="mt-6 space-y-3 text-sm text-slate-300">
            <PlanItem>Daily multilingual trend post (EN/ES/JA)</PlanItem>
            <PlanItem>Top-3 trending videos, twice a week</PlanItem>
            <PlanItem>Community access</PlanItem>
          </ul>
          <a
            href="#"
            className="mt-8 block w-full rounded-full border border-white/15 py-3 text-center text-sm font-semibold text-white transition hover:border-white/30 hover:bg-white/5"
          >
            Get Started
          </a>
        </div>

        {/* Paid plan */}
        <div className="relative overflow-hidden rounded-2xl border border-neon-purple/40 bg-white/[0.04] p-8 shadow-glow">
          <div className="absolute right-6 top-6 rounded-full bg-cta-gradient px-3 py-1 text-[11px] font-semibold text-white">
            Most Popular
          </div>
          <h3 className="text-sm font-semibold uppercase tracking-wide text-neon-purple">
            Pro
          </h3>
          <div className="mt-3 flex items-baseline gap-1">
            <span className="text-4xl font-extrabold text-white">$29</span>
            <span className="text-sm text-slate-500">/mo</span>
          </div>
          <ul className="mt-6 space-y-3 text-sm text-slate-300">
            <PlanItem>Full daily deep-dive newsletter</PlanItem>
            <PlanItem>Every trending video, every region</PlanItem>
            <PlanItem>Priority multilingual social drafts</PlanItem>
            <PlanItem>Cancel anytime</PlanItem>
          </ul>
          {/* Wire STRIPE_PAYMENT_LINK to a real Stripe Payment Link (or
              Checkout Session URL) via the VITE_STRIPE_PAYMENT_LINK env var
              before deploying — this placeholder does not process payment. */}
          <a
            href={STRIPE_PAYMENT_LINK}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-8 block w-full rounded-full bg-cta-gradient py-3 text-center text-sm font-semibold text-white transition hover:shadow-glow-blue"
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
      <svg viewBox="0 0 20 20" fill="none" className="mt-0.5 h-4 w-4 shrink-0 text-electric-blue">
        <path
          d="M4 10l4 4 8-8"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      {children}
    </li>
  );
}
