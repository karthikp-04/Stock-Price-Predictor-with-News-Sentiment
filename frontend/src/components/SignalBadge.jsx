// src/components/SignalBadge.jsx
export default function SignalBadge({ signal, type }) {
  const icon = type === 'buy' ? '▲' : type === 'sell' ? '▼' : '■';

  return (
    <span className={`signal-badge ${type}`} id={`signal-badge-${type}`}>
      <span className="signal-dot" />
      <span>{icon} {signal}</span>
    </span>
  );
}
