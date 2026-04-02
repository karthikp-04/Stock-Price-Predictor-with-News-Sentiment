# app/api/server.py — StockSense AI Backend
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import sys
import json
from dotenv import load_dotenv

# ── Path Setup ──────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

from app.ml.predictor import HybridStockPredictor

# ── Constants ───────────────────────────────────────────────────
WATCHLIST_FILE = os.path.join(PROJECT_ROOT, 'data', 'watchlist.json')

# ── App ─────────────────────────────────────────────────────────
app = FastAPI(
    title="StockSense AI API",
    description="Hybrid Stock Prediction with FinBERT & Technical Analysis",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global State ────────────────────────────────────────────────
predictor = None

# ── Models ──────────────────────────────────────────────────────
class WatchlistAdd(BaseModel):
    ticker: str

# ── Watchlist Helpers ───────────────────────────────────────────
def load_watchlist():
    try:
        if os.path.exists(WATCHLIST_FILE):
            with open(WATCHLIST_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {"tickers": ["AAPL", "TSLA", "GOOGL"]}

def save_watchlist(data):
    os.makedirs(os.path.dirname(WATCHLIST_FILE), exist_ok=True)
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ── Lifecycle ───────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    global predictor
    news_key = os.getenv("NEWS_API_KEY", "")
    finnhub_key = os.getenv("FINNHUB_KEY", "")
    predictor = HybridStockPredictor(news_key, finnhub_key)
    print("[OK] StockSense AI - Predictor initialized")

# ── Core Endpoints ──────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "app": "StockSense AI",
        "version": "2.0.0",
        "status": "running",
        "endpoints": ["/predict/{ticker}", "/stock/{ticker}",
                      "/sentiment/{ticker}", "/watchlist"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "predictor_ready": predictor is not None}

@app.get("/predict/{ticker}")
async def predict(ticker: str):
    """Full hybrid prediction for a ticker."""
    if not predictor:
        raise HTTPException(503, "Predictor not initialized")
    try:
        result = predictor.predict_stock(ticker.upper())
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/stock/{ticker}")
async def stock_data(ticker: str):
    """Get live stock price data."""
    if not predictor:
        raise HTTPException(503, "Predictor not initialized")
    try:
        hist, info = predictor.get_stock_data(ticker.upper())
        if hist is None:
            raise HTTPException(404, f"No data for {ticker}")

        current = round(float(hist['Close'].iloc[-1]), 2)
        prev = round(float(hist['Close'].iloc[-2]), 2) if len(hist) > 1 else current

        return {
            'ticker': ticker.upper(),
            'current_price': current,
            'prev_close': prev,
            'change': round(current - prev, 2),
            'change_pct': round(((current - prev) / prev) * 100, 2) if prev else 0,
            'info': info
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/sentiment/{ticker}")
async def sentiment(ticker: str):
    """Get FinBERT sentiment analysis for a ticker."""
    if not predictor:
        raise HTTPException(503, "Predictor not initialized")
    try:
        headlines = predictor.get_news_headlines(ticker.upper())
        score, details = predictor.analyze_sentiment_finbert(headlines)
        return {
            'ticker': ticker.upper(),
            'sentiment_score': score,
            'news_count': len(details),
            'headlines': details
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/stocks/popular")
async def popular_stocks():
    return {"stocks": ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NVDA", "NFLX"]}

# ── Watchlist Endpoints ─────────────────────────────────────────
@app.get("/watchlist")
async def get_watchlist():
    return load_watchlist()

@app.post("/watchlist")
async def add_to_watchlist(item: WatchlistAdd):
    data = load_watchlist()
    ticker = item.ticker.upper()
    if ticker not in data['tickers']:
        data['tickers'].append(ticker)
        save_watchlist(data)
    return data

@app.delete("/watchlist/{ticker}")
async def remove_from_watchlist(ticker: str):
    data = load_watchlist()
    ticker = ticker.upper()
    if ticker in data['tickers']:
        data['tickers'].remove(ticker)
        save_watchlist(data)
    return data

@app.get("/watchlist/predictions")
async def watchlist_predictions():
    """Batch predictions for all watchlist items."""
    if not predictor:
        raise HTTPException(503, "Predictor not initialized")

    data = load_watchlist()
    results = []
    for t in data.get('tickers', []):
        try:
            result = predictor.predict_stock(t)
            results.append(result)
        except Exception as e:
            results.append({'ticker': t, 'error': str(e)})
    return {'predictions': results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)