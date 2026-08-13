# Go-Live Checklist

Everything code-side is done and verified (build passes, imports succeed,
Dockerfiles are written and ready for either platform below). What's left
is entirely account/credential creation — steps only you can do, because
they require your identity, payment method, or a domain you own. Each step
is written so you can do it in one sitting with no side-decisions.

## 1. Get your 4 API keys (~15 min)

- [ ] **Anthropic** — [console.anthropic.com](https://console.anthropic.com) → Settings → API Keys → Create Key. Copy it.
- [ ] **YouTube Data API v3** — [console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials) → New Project → APIs & Services → Library → search "YouTube Data API v3" → Enable → Credentials → Create Credentials → API Key. Copy it. (Free, 10,000 units/day.)
- [ ] **Stripe** — [dashboard.stripe.com/register](https://dashboard.stripe.com/register) → after signup: Developers → API keys → copy the **Secret key**. Then Product catalog → Add product → name "TrendPulse Pro", price **$29.00/month recurring** → Save → copy the **Price ID** (`price_...`) shown on the product page. Then Payment Links → Create payment link → select the TrendPulse Pro price → Create → copy the link URL (this goes into the frontend's `VITE_STRIPE_PAYMENT_LINK`).
- [ ] **Mailgun** — [signup.mailgun.com](https://signup.mailgun.com) → Sending → Domains → Add New Domain (or use the sandbox domain to test immediately, no DNS needed) → if using your own domain, add the shown DNS TXT/CNAME/MX records at your domain registrar → copy the **API key** (Settings → API Keys) and the **domain name**.

## 2. Deploy the backend (Railway — Dockerfile already included, ~5 min)

- [ ] [railway.app](https://railway.app) → New Project → Deploy from GitHub repo (push this `trendpulse/` folder to a GitHub repo first) → select the repo, set **Root Directory** to `backend`.
- [ ] Railway auto-detects `backend/Dockerfile` and `railway.json` — no build config needed.
- [ ] Variables tab → paste in all values from `backend/.env.example` (with your real keys from step 1). Leave `DB_PATH` as-is.
- [ ] Generate a random string for `INTERNAL_TRIGGER_TOKEN` — e.g. run `openssl rand -hex 32` locally and paste the output.
- [ ] After first deploy succeeds, copy the public Railway URL (e.g. `https://trendpulse-backend-production.up.railway.app`) — you'll need it in step 3.
- [ ] Back in Stripe (step 1) → Developers → Webhooks → Add endpoint → URL = `<railway-url>/webhooks/stripe`, events = `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted` → copy the **Signing secret** (`whsec_...`) → add it to Railway's `STRIPE_WEBHOOK_SECRET` variable and redeploy.

## 3. Deploy the frontend (Vercel — zero config, ~3 min)

- [ ] [vercel.com/new](https://vercel.com/new) → Import the same GitHub repo → set **Root Directory** to `frontend` → Vercel auto-detects Vite.
- [ ] Environment Variables → add `VITE_API_BASE_URL` = the Railway URL from step 2, and `VITE_STRIPE_PAYMENT_LINK` = the Payment Link from step 1 → Deploy.
- [ ] Copy the resulting `*.vercel.app` URL (or attach your own domain in Vercel's Domains tab).
- [ ] Go back to Railway → Variables → set `LP_BASE_URL` to this frontend URL, and `CORS_ORIGINS` to the same URL → redeploy.

## 4. Turn on the daily automation (~2 min)

The backend never runs the pipeline on its own — something has to call it.
Easiest option: a free scheduled GitHub Action in the same repo.

- [ ] Create `.github/workflows/daily-trigger.yml` in the repo:
  ```yaml
  name: TrendPulse Daily Trigger
  on:
    schedule:
      - cron: "0 13 * * *"  # 13:00 UTC daily — adjust to your preferred time
    workflow_dispatch: {}
  jobs:
    trigger:
      runs-on: ubuntu-latest
      steps:
        - run: |
            curl -X POST "${{ secrets.TRENDPULSE_API_URL }}/internal/run-cycle" \
              -H "X-Internal-Token: ${{ secrets.TRENDPULSE_INTERNAL_TOKEN }}"
  ```
- [ ] Repo Settings → Secrets and variables → Actions → add `TRENDPULSE_API_URL` (the Railway URL) and `TRENDPULSE_INTERNAL_TOKEN` (the same value as `INTERNAL_TRIGGER_TOKEN`).
- [ ] Test it immediately: Actions tab → "TrendPulse Daily Trigger" → Run workflow (uses the `workflow_dispatch` trigger, no need to wait for the cron).

## 5. Verify it actually works end-to-end

- [ ] Open the Vercel URL → submit the "Start Free Trial" form with your own email → check Railway logs for a successful `/signup` request.
- [ ] Manually trigger step 4's workflow once → check Railway logs for `AutomationWorkflow: saved issue #1`.
- [ ] Pay yourself $29 via the Stripe Payment Link (Stripe test mode lets you use card `4242 4242 4242 4242` with any future date/CVC to test for free) → check that your email appears as a `pro` subscriber (Stripe Dashboard → Customers, or query the backend's SQLite DB) → trigger the workflow again → confirm you receive the newsletter email.

---

Everything above this line needs your accounts. Everything below is already
done and needs nothing further from you:
- All backend agents, DB schema, FastAPI routes, Stripe signature verification
- All frontend components, dark-mode design, interactive demo
- Both Dockerfiles, `railway.json`, `docker-compose.yml` for local testing
- `.env.example` files listing every variable by name
