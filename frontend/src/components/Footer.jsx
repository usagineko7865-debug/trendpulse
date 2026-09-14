export default function Footer() {
  return (
    <footer className="border-t border-line px-6 py-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 text-sm text-ink-faint sm:flex-row">
        <div className="flex items-center gap-2">
          <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-coral text-white">
            <svg viewBox="0 0 24 24" className="h-3.5 w-3.5" fill="none">
              <path
                d="M3 12h4l2-7 4 14 2-7h6"
                stroke="currentColor"
                strokeWidth="2.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <span className="font-display font-semibold text-ink-soft">TrendPulse</span>
        </div>
        <p>&copy; {new Date().getFullYear()} TrendPulse. Fully autonomous, no humans in the loop.</p>
      </div>
    </footer>
  );
}
