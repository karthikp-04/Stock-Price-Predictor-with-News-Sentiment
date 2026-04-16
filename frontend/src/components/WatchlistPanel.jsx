// src/components/WatchlistPanel.jsx
import { useState } from 'react';
import { Plus, X, TrendingUp } from 'lucide-react';
import { addToWatchlist, removeFromWatchlist } from '../api/stockApi';

export default function WatchlistPanel({ watchlist, setWatchlist, onSelect, activeTicker }) {
  const [newTicker, setNewTicker] = useState('');
  const [adding, setAdding] = useState(false);

  const handleAdd = async () => {
    const t = newTicker.trim().toUpperCase();
    if (!t) return;
    setAdding(true);
    try {
      const data = await addToWatchlist(t);
      setWatchlist(data.tickers || []);
      setNewTicker('');
    } catch (e) {
      console.error('Add failed:', e);
    }
    setAdding(false);
  };

  const handleRemove = async (ticker) => {
    try {
      const data = await removeFromWatchlist(ticker);
      setWatchlist(data.tickers || []);
    } catch (e) {
      console.error('Remove failed:', e);
    }
  };

  return (
    <div className="card watchlist-panel" id="watchlist-panel">
      <h3>
        <TrendingUp size={14} style={{ marginRight: 6 }} />
        Watchlist
      </h3>

      {/* Add Input */}
      <div className="watchlist-add">
        <input
          value={newTicker}
          onChange={(e) => setNewTicker(e.target.value.toUpperCase())}
          onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
          placeholder="Add ticker…"
          maxLength={10}
          id="watchlist-add-input"
        />
        <button onClick={handleAdd} disabled={adding || !newTicker.trim()} id="watchlist-add-btn">
          <Plus size={18} />
        </button>
      </div>

      {/* Items */}
      <div className="watchlist-items">
        {watchlist.length === 0 && (
          <div className="watchlist-empty">
            <span>No stocks yet</span>
          </div>
        )}
        {watchlist.map((ticker) => (
          <div
            key={ticker}
            className={`watchlist-item ${activeTicker === ticker ? 'active' : ''}`}
            onClick={() => onSelect(ticker)}
          >
            <span className="ticker">{ticker}</span>
            <button
              className="remove-btn"
              onClick={(e) => { e.stopPropagation(); handleRemove(ticker); }}
              aria-label={`Remove ${ticker}`}
            >
              <X size={14} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
