// src/components/Navbar.jsx
import { useState, useEffect } from 'react';
import { Search, Activity } from 'lucide-react';
import { checkHealth } from '../api/stockApi';

const POPULAR = ['AAPL', 'TSLA', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'META', 'NFLX'];

export default function Navbar({ onSearch, loading }) {
  const [ticker, setTicker] = useState('');
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    checkHealth()
      .then(() => setConnected(true))
      .catch(() => setConnected(false));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (ticker.trim() && !loading) {
      onSearch(ticker.trim().toUpperCase());
    }
  };

  const quickSearch = (t) => {
    setTicker(t);
    onSearch(t);
  };

  return (
    <nav className="navbar" id="main-navbar">
      <div className="navbar-brand">
        <span className="logo">🔮</span>
        <div>
          <h1>StockSense AI</h1>
        </div>
        <span className="version">v2.0</span>
      </div>

      <div className="search-container" id="search-container">
        <form onSubmit={handleSubmit}>
          <div className="search-input-wrapper">
            <Search className="search-icon" size={16} />
            <input
              className="search-input"
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              placeholder="Search ticker… (e.g. AAPL)"
              maxLength={10}
              id="ticker-search-input"
            />
            <button
              className="search-btn"
              type="submit"
              disabled={loading || !ticker.trim()}
              id="predict-button"
            >
              {loading ? 'Analyzing…' : 'Predict'}
            </button>
          </div>
        </form>

        <div className="popular-tags">
          <span>Popular:</span>
          {POPULAR.map((s) => (
            <button key={s} className="popular-tag" onClick={() => quickSearch(s)}>
              {s}
            </button>
          ))}
        </div>
      </div>

      <div className="status-indicator" id="api-status">
        <span className={`status-dot ${connected ? 'connected' : 'disconnected'}`} />
        <Activity size={14} />
        <span>{connected ? 'API Connected' : 'API Offline'}</span>
      </div>
    </nav>
  );
}
