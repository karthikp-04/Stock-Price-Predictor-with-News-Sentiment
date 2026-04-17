// src/App.jsx — StockSense AI Main Application
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import PredictionCard from './components/PredictionCard';
import SentimentPanel from './components/SentimentPanel';
import PriceChart from './components/PriceChart';
import WatchlistPanel from './components/WatchlistPanel';
import { fetchPrediction, fetchWatchlist } from './api/stockApi';
import './App.css';

export default function App() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [watchlist, setWatchlist] = useState([]);
  const [activeTicker, setActiveTicker] = useState('');

  // Load watchlist on mount
  useEffect(() => {
    fetchWatchlist()
      .then((data) => setWatchlist(data.tickers || []))
      .catch(() => setWatchlist(['AAPL', 'TSLA', 'GOOGL']));
  }, []);

  // Search handler
  const handleSearch = async (ticker) => {
    setLoading(true);
    setError(null);
    setActiveTicker(ticker);
    try {
      const result = await fetchPrediction(ticker);
      if (result.error) {
        setError(result.error);
        setPrediction(null);
      } else {
        setPrediction(result);
      }
    } catch (e) {
      setError(e.message || 'Failed to fetch prediction');
      setPrediction(null);
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <Navbar onSearch={handleSearch} loading={loading} />

      <main className="main-content">
        <div className="content-grid">
          {/* Left Column */}
          <div className="left-column">
            {loading && <LoadingCard ticker={activeTicker} />}
            {error && !loading && <ErrorCard message={error} onRetry={() => handleSearch(activeTicker)} />}
            {prediction && !loading && !error && (
              <>
                <PredictionCard data={prediction} />
                <div className="bottom-row">
                  <SentimentPanel data={prediction.sentiment} />
                  <PriceChart data={prediction.chart_data} ticker={prediction.ticker} />
                </div>
              </>
            )}
            {!prediction && !loading && !error && <WelcomeCard />}
          </div>

          {/* Right Column */}
          <div className="right-column">
            <WatchlistPanel
              watchlist={watchlist}
              setWatchlist={setWatchlist}
              onSelect={handleSearch}
              activeTicker={activeTicker}
            />
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>StockSense AI · Powered by FinBERT + yfinance · Not financial advice</p>
      </footer>
    </div>
  );
}

/* ── Inline helper components ────────────────────────────────── */

function WelcomeCard() {
  return (
    <div className="card welcome-card" id="welcome-card">
      <div className="welcome-icon">🔮</div>
      <h2>Welcome to StockSense AI</h2>
      <p>
        Search any stock ticker above to get an AI-powered prediction using
        FinBERT sentiment analysis and technical indicators.
      </p>
      <div className="welcome-features">
        <div className="feature">
          <span className="feature-icon">📰</span>
          <span>FinBERT NLP Sentiment</span>
        </div>
        <div className="feature">
          <span className="feature-icon">📊</span>
          <span>RSI · MACD · MA Crossover</span>
        </div>
        <div className="feature">
          <span className="feature-icon">⚖️</span>
          <span>Dynamic 70/30 Weighting</span>
        </div>
      </div>
    </div>
  );
}

function LoadingCard({ ticker }) {
  return (
    <div className="card loading-card" id="loading-card">
      <div className="spinner" />
      <p>Analyzing <strong>{ticker}</strong>…</p>
      <span className="loading-sub">Fetching price data, news sentiment & technical indicators</span>
    </div>
  );
}

function ErrorCard({ message, onRetry }) {
  return (
    <div className="card error-card" id="error-card">
      <div className="error-icon">⚠️</div>
      <p>{message}</p>
      <button className="retry-btn" onClick={onRetry}>Try Again</button>
    </div>
  );
}
