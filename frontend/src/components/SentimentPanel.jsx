// src/components/SentimentPanel.jsx
export default function SentimentPanel({ data }) {
  if (!data) return null;

  const { score, news_count, details } = data;

  const getColor = (s) =>
    s > 0.1 ? 'var(--signal-buy)' :
    s < -0.1 ? 'var(--signal-sell)' :
    'var(--signal-hold)';

  const getLabel = (s) =>
    s > 0.3  ? 'Very Bullish' :
    s > 0.1  ? 'Bullish' :
    s < -0.3 ? 'Very Bearish' :
    s < -0.1 ? 'Bearish' :
    'Neutral';

  const barLeft = ((score + 1) / 2) * 100;

  return (
    <div className="card sentiment-panel" id="sentiment-panel">
      <h3>FinBERT Sentiment</h3>

      {/* Score */}
      <div className="sentiment-score">
        <div className="score-value" style={{ color: getColor(score) }}>
          {score > 0 ? '+' : ''}{score.toFixed(3)}
        </div>
        <div className="score-label" style={{ color: getColor(score) }}>
          {getLabel(score)}
        </div>
        <div className="score-count">
          {news_count} article{news_count !== 1 ? 's' : ''} analyzed
        </div>
      </div>

      {/* Sentiment Bar */}
      <div className="sentiment-bar">
        <div className="bar-track">
          <div
            className="bar-indicator"
            style={{
              left: `${barLeft}%`,
              backgroundColor: getColor(score),
            }}
          />
        </div>
        <div className="bar-labels">
          <span>Bearish</span>
          <span>Neutral</span>
          <span>Bullish</span>
        </div>
      </div>

      {/* Headlines */}
      <div className="headline-list">
        {details && details.map((item, i) => (
          <div key={i} className="headline-item">
            <span className={`headline-badge ${item.label}`}>
              {item.label === 'positive' ? '↑' : item.label === 'negative' ? '↓' : '→'}
            </span>
            <div className="headline-content">
              <p className="headline-text">{item.headline}</p>
              <span className="headline-meta">
                {item.source} · {item.published}
              </span>
            </div>
            <span className={`headline-score ${item.label}`}>
              {(item.confidence * 100).toFixed(0)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
