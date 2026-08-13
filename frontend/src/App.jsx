import Hero from "./components/Hero.jsx";
import Features from "./components/Features.jsx";
import InteractivePreview from "./components/InteractivePreview.jsx";
import Pricing from "./components/Pricing.jsx";
import Footer from "./components/Footer.jsx";

export default function App() {
  return (
    <div className="relative min-h-screen overflow-x-hidden bg-ink-950">
      {/* ambient background glow, shared across the page */}
      <div className="pointer-events-none fixed inset-0 bg-grid-glow" />
      <div className="pointer-events-none fixed -top-40 right-0 h-96 w-96 rounded-full bg-electric-blue/10 blur-3xl" />

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
