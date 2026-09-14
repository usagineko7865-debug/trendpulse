/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#FBF4E7",
        "paper-soft": "#F3E8D3",
        card: "#FFFDF8",
        ink: {
          DEFAULT: "#2A2318",
          soft: "#6E6353",
          faint: "#A69A85",
        },
        coral: {
          DEFAULT: "#FF5B3C",
          deep: "#E0431F",
          soft: "#FFE2D3",
        },
        teal: {
          DEFAULT: "#106B60",
          soft: "#DCECE6",
        },
        line: "#E9DBBE",
      },
      fontFamily: {
        display: ["Fredoka", "sans-serif"],
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
      },
      boxShadow: {
        card: "0 2px 0 0 rgba(42,35,24,0.06), 0 12px 30px -12px rgba(42,35,24,0.18)",
        pop: "0 10px 28px -8px rgba(255,91,60,0.45)",
        lift: "0 20px 50px -20px rgba(42,35,24,0.25)",
      },
      borderRadius: {
        xl2: "1.75rem",
      },
    },
  },
  plugins: [],
};
