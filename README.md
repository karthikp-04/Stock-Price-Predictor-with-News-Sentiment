# StockSense AI — Hybrid Stock Predictor

A full-stack stock prediction platform using **FinBERT** sentiment analysis and technical indicators (RSI, MACD, MA Crossover) with dynamic weighting logic.

## Features

- **FinBERT NLP Sentiment** — Real-time financial news analysis using ProsusAI/finbert
- **Technical Analysis** — RSI (14), MACD, Moving Average crossover
- **Dynamic Weighting** — 70% News / 30% Technical when recent news exists; 100% Technical otherwise
- **Interactive Dashboard** — React frontend with dark glassmorphism UI
- **Watchlist Management** — Save and track your favorite tickers
- **Live Data** — Real-time prices from yfinance, news from NewsAPI

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, FinBERT (transformers), yfinance, NumPy, Pandas |
| Frontend | React (Vite), Recharts, Lucide Icons |
| APIs | NewsAPI, Finnhub, Yahoo Finance |

## Architecture

```
StockMarketPredictor/
├── app/
│   ├── api/
│   │   └── server.py          # FastAPI endpoints
│   └── ml/
│       └── predictor.py       # FinBERT + technical analysis
├── frontend/
│   └── src/
│       ├── App.jsx            # Main dashboard
│       ├── components/        # React components
│       └── api/stockApi.js    # API client
├── data/                      # Runtime data (watchlist)
├── main.py                    # Entry point
└── requirements.txt           # Python dependencies
```

## Setup & Run

### Prerequisites
- Python 3.10+
- Node.js 18+
- API keys from [NewsAPI](https://newsapi.org/register) and [Finnhub](https://finnhub.io/register)

### 1. Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install --upgrade yfinance

# Create .env file
echo "NEWS_API_KEY=your_newsapi_key" > .env
echo "FINNHUB_KEY=your_finnhub_key" >> .env

# Start server
uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000** in your browser.

## How It Works

1. User searches a stock ticker (e.g., AAPL)
2. Backend fetches live price data from yfinance
3. News headlines are fetched from NewsAPI
4. **FinBERT** classifies each headline as positive/negative/neutral
5. Technical indicators (RSI, MACD, MA) are computed
6. Dynamic weighting combines signals: **70% sentiment + 30% technical** (or 100% technical if no news)
7. Final BUY/SELL/HOLD signal with confidence score is returned
8. React dashboard displays the prediction with charts and details

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /predict/{ticker}` | Full hybrid prediction |
| `GET /stock/{ticker}` | Live stock data |
| `GET /sentiment/{ticker}` | FinBERT sentiment breakdown |
| `GET /watchlist` | Get saved watchlist |
| `POST /watchlist` | Add ticker to watchlist |
| `DELETE /watchlist/{ticker}` | Remove from watchlist |

## Screenshots

_Run the app locally to see the interactive dashboard._

## License

MIT
