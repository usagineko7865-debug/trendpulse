export default function PulseLine({ className = "" }) {
  return (
    <svg
      viewBox="0 0 400 40"
      fill="none"
      className={className}
      preserveAspectRatio="none"
    >
      <path
        d="M0 20 H130 L148 6 L166 34 L182 14 L194 20 H400"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
