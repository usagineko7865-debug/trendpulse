import { useState } from "react";

/**
 * This preview is an intentional client-side MOCK — it does not call the
 * real backend/LLM. Wiring a live Claude call to an unauthenticated public
 * form would let anyone on the internet spend the site owner's API budget
 * for free. The real generation pipeline (ContentGeneratorAgent) is fully
 * implemented server-side; this component just demonstrates what it
 * produces, deterministically, from canned output.
 */
const MOCK_RESULT = {
  en: "🚨 A tiny startup just shipped an on-device AI model that beats GPT-4 on coding benchmarks — using 1/50th the compute. Here's why builders are paying attention.",
  es: "🚨 Una pequeña startup lanzó un modelo de IA local que supera a GPT-4 en benchmarks de código — usando 1/50 del cómputo. Así es como los desarrolladores están reaccionando.",
  ja: "🚨 小さなスタートアップが、GPT-4を上回るコーディング性能を持つオンデバイスAIモデルを、わずか1/50の計算量で実現。エンジニアたちが今注目する理由とは。",
};

function isLikelyYoutubeUrl(value) {
  return /youtu\.?be/i.test(value);
}

export default function InteractivePreview() {
  const [url, setUrl] = useState("");
  const [stage, setStage] = useState("idle"); // idle | scraping | generating | done
  const [lang, setLang] = useState("en");

  function handleRun(e) {
    e.preventDefault();
    if (!url) return;
    setStage("scraping");
    setTimeout(() => setStage("generating"), 900);
    setTimeout(() => setStage("done"), 2000);
  }

  return (
    <section className="mx-auto max-w-6xl px-6 py-20">
      <div className="mx-auto mb-12 max-w-2xl text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal">
          Try it yourself
        </p>
        <h2 className="mt-3 font-display text-3xl font-semibold tracking-tight text-ink sm:text-4xl">
          See the transformation
        </h2>
        <p className="mt-4 text-ink-soft">
          Paste any trending video URL and watch how TrendPulse would turn it
          into a viral multilingual post.{" "}
          <span className="text-ink-faint">(Interactive demo — simulated output.)</span>
        </p>
      </div>

      <div className="mx-auto max-w-3xl rounded-xl2 border border-line bg-card p-6 shadow-card sm:p-8">
        <form onSubmit={handleRun} className="flex flex-col gap-3 sm:flex-row">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://youtube.com/watch?v=..."
            className="w-full rounded-full border-2 border-line bg-paper px-5 py-3 text-sm text-ink placeholder-ink-faint outline-none transition focus:border-teal"
          />
          <button
            type="submit"
            disabled={stage === "scraping" || stage === "generating"}
            className="shrink-0 rounded-full bg-ink px-6 py-3 text-sm font-semibold text-paper transition hover:bg-teal disabled:opacity-50"
          >
            {stage === "idle" || stage === "done" ? "Transform ✨" : "Working…"}
          </button>
        </form>

        {url && !isLikelyYoutubeUrl(url) && stage === "idle" && (
          <p className="mt-2 text-xs text-coral-deep">
            Tip: paste a YouTube URL for the most realistic demo.
          </p>
        )}

        {stage !== "idle" && (
          <div className="mt-8 space-y-4">
            <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-ink-soft">
              <StepDot active={stage !== "idle"} label="Scraping trend data" />
              <StepDot
                active={stage === "generating" || stage === "done"}
                label="Generating multilingual copy"
              />
              <StepDot active={stage === "done"} label="Ready" />
            </div>

            {stage === "done" && (
              <div className="rounded-xl border border-line bg-paper-soft p-5">
                <div className="mb-4 flex gap-2">
                  {["en", "es", "ja"].map((l) => (
                    <button
                      key={l}
                      onClick={() => setLang(l)}
                      className={`rounded-full px-3 py-1 text-xs font-semibold uppercase transition ${
                        lang === l
                          ? "bg-coral text-white"
                          : "bg-card text-ink-soft hover:bg-card/70"
                      }`}
                    >
                      {l}
                    </button>
                  ))}
                </div>
                <p className="text-sm leading-relaxed text-ink">
                  {MOCK_RESULT[lang]}
                </p>
                <p className="mt-4 truncate text-xs text-teal">
                  https://trendpulse.example.com?utm_source=social&utm_medium=auto&utm_campaign=trend
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
}

function StepDot({ active, label }) {
  return (
    <span className="flex items-center gap-1.5">
      <span
        className={`h-1.5 w-1.5 rounded-full transition ${
          active ? "bg-coral" : "bg-line"
        }`}
      />
      <span className={active ? "text-ink" : ""}>{label}</span>
    </span>
  );
}
