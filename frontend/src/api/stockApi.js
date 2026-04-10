// src/api/stockApi.js — API Client for StockSense AI Backend
const API_BASE = 'http://localhost:8000';

async function request(url, options = {}) {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed (${response.status})`);
  }
  return response.json();
}

// ── Core Endpoints ──────────────────────────────────────────────
export const fetchPrediction   = (ticker) => request(`/predict/${ticker}`);
export const fetchStockData    = (ticker) => request(`/stock/${ticker}`);
export const fetchSentiment    = (ticker) => request(`/sentiment/${ticker}`);
export const fetchPopular      = ()       => request('/stocks/popular');
export const checkHealth       = ()       => request('/health');

// ── Watchlist ───────────────────────────────────────────────────
export const fetchWatchlist    = ()       => request('/watchlist');

export const addToWatchlist    = (ticker) =>
  request('/watchlist', {
    method: 'POST',
    body: JSON.stringify({ ticker }),
  });

export const removeFromWatchlist = (ticker) =>
  request(`/watchlist/${ticker}`, { method: 'DELETE' });
