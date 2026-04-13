// src/components/PredictionCard.jsx
import SignalBadge from './SignalBadge';

export default function PredictionCard({ data }) {
  const {
    ticker, name, current_price, change, change_pct,
    signal, signal_type, confidence, weights, technical
  } = data;

  const positive = change >= 0;

  return (
    <div className={`card prediction-card signal-${signal_type}`} id="prediction-card">
      {/* Header */}
      <div className="prediction-header">
        <div className="ticker-info">
          <h2 className="ticker-symbol">{ticker}</h2>
          <span className="company-name">{name}</span>
        </div>
        <SignalBadge signal={signal} type={signal_type} />
      </div>

      {/* Price */}
      <div className="price-info">
        <span className="current-price">${current_price?.toFixed(2)}</span>
        <span className={`price-change ${positive ? 'positive' : 'negative'}`}>
          {positive ? '+' : ''}{change?.toFixed(2)} ({change_pct?.toFixed(2)}%)
        </span>
      </div>

      {/* Confidence Bar */}
      <div className="confidence-section">
        <div className="confidence-label">
          <span>Confidence</span>
          <span className="confidence-value">{(confidence * 100).toFixed(1)}%</span>
        </div>
        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{
              width: `${confidence * 100}%`,
              backgroundColor:
                signal_type === 'buy'  ? 'var(--signal-buy)' :
                signal_type === 'sell' ? 'var(--signal-sell)' :
                                         'var(--signal-hold)',
            }}
          />
        </div>
      </div>

      {/* Weight Breakdown */}
      <div className="weights-section">
        <div className="weights-title">Signal Weighting</div>
        <div className="weight-bar">
          {weights.news > 0 && (
            <div className="weight-news" style={{ width: `${weights.news * 100}%` }}>
              📰 News {Math.round(weights.news * 100)}%
            </div>
          )}
          <div className="weight-tech" style={{ width: `${weights.technical * 100}%` }}>
            📊 Technical {Math.round(weights.technical * 100)}%
          </div>
        </div>
      </div>

      {/* Tech Indicators */}
      {technical && Object.keys(technical).length > 0 && (
        <div className="tech-details">
          {technical.ma_crossover && (
            <div className="tech-item">
              <span className="label">MA Cross</span>
              <span className={`value ${technical.ma_crossover === 'bullish' ? 'positive' : 'negative'}`}>
                {technical.ma_crossover === 'bullish' ? '↑' : '↓'} {technical.ma_crossover}
              </span>
            </div>
          )}
          {technical.rsi !== undefined && (
            <div className="tech-item">
              <span className="label">RSI (14)</span>
              <span className="value">{technical.rsi}</span>
            </div>
          )}
          {technical.macd && (
            <div className="tech-item">
              <span className="label">MACD</span>
              <span className={`value ${technical.macd === 'bullish' ? 'positive' : 'negative'}`}>
                {technical.macd === 'bullish' ? '↑' : '↓'} {technical.macd}
              </span>
            </div>
          )}
          {technical.five_day_change !== undefined && (
            <div className="tech-item">
              <span className="label">5-Day</span>
              <span className={`value ${technical.five_day_change >= 0 ? 'positive' : 'negative'}`}>
                {technical.five_day_change >= 0 ? '+' : ''}{technical.five_day_change}%
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
