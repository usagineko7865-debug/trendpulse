export default function Footer() {
  return (
    <footer className="border-t border-white/5 px-6 py-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 text-sm text-slate-500 sm:flex-row">
        <div className="flex items-center gap-2">
          <div className="h-5 w-5 rounded bg-cta-gradient" />
          <span className="font-semibold text-slate-300">TrendPulse</span>
        </div>
        <p>&copy; {new Date().getFullYear()} TrendPulse. Fully autonomous, no humans in the loop.</p>
      </div>
    </footer>
  );
}
