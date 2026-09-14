import Hero from "./components/Hero.jsx";
import Features from "./components/Features.jsx";
import InteractivePreview from "./components/InteractivePreview.jsx";
import Pricing from "./components/Pricing.jsx";
import Footer from "./components/Footer.jsx";

export default function App() {
  return (
    <div className="relative min-h-screen overflow-x-hidden bg-paper">
      {/* soft warm glow, shared across the page — replaces the old moody dark-mode gradient */}
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(255,91,60,0.10),transparent_55%)]" />
      <div className="pointer-events-none fixed -top-32 -right-24 h-96 w-96 rounded-full bg-teal/10 blur-3xl" />

      <div className="relative">
        <Hero />
        <Features />
        <InteractivePreview />
        <Pricing />
        <Footer />
      </div>
    </div>
  );
}
