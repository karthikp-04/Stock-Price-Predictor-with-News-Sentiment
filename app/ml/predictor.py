# app/ml/predictor.py
# Hybrid Stock Predictor with FinBERT Sentiment Analysis
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import warnings
warnings.filterwarnings('ignore')

# ── FinBERT Lazy Loader ────────────────────────────────────────
_finbert_pipeline = None
_finbert_loaded = False

def get_finbert():
    """Lazy-load FinBERT model (downloads ~400MB on first run, then cached)."""
    global _finbert_pipeline, _finbert_loaded
    if not _finbert_loaded:
        try:
            from transformers import pipeline as hf_pipeline
            _finbert_pipeline = hf_pipeline(
                "sentiment-analysis",
                model="ProsusAI/finbert",
                tokenizer="ProsusAI/finbert",
                device=-1  # Force CPU
            )
            print("[OK] FinBERT model loaded successfully")
        except Exception as e:
            print(f"[WARN] FinBERT unavailable, using keyword fallback: {e}")
            _finbert_pipeline = None
        _finbert_loaded = True
    return _finbert_pipeline


# ── Main Predictor Class ───────────────────────────────────────
class HybridStockPredictor:
    def __init__(self, news_api_key, finnhub_key):
        self.news_api_key = news_api_key
        self.finnhub_key = finnhub_key

    # ── Stock Data ──────────────────────────────────────────────
    def get_stock_data(self, ticker):
        """Get stock data using yfinance."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo")

            if len(hist) < 5:
                return None, None

            current_price = hist['Close'].iloc[-1]
            print(f"[PRICE] {ticker}: ${current_price:.2f}")

            info = {}
            try:
                raw = stock.info
                info = {
                    'name': raw.get('shortName', ticker),
                    'sector': raw.get('sector', 'N/A'),
                    'market_cap': raw.get('marketCap', 0),
                    'pe_ratio': raw.get('trailingPE', 0),
                    'fifty_two_high': raw.get('fiftyTwoWeekHigh', 0),
                    'fifty_two_low': raw.get('fiftyTwoWeekLow', 0),
                }
            except Exception:
                info = {'name': ticker}

            return hist, info

        except Exception as e:
            print(f"[ERROR] Error getting {ticker}: {e}")
            return None, None

    # ── News Headlines ──────────────────────────────────────────
    def get_news_headlines(self, ticker):
        """Fetch financial news headlines from NewsAPI."""
        headlines = []
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': ticker,
                'apiKey': self.news_api_key,
                'pageSize': 10,
                'language': 'en',
                'sortBy': 'publishedAt'
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data.get('status') == 'ok':
                for article in data.get('articles', []):
                    title = article.get('title', '')
                    if title and title != '[Removed]':
                        headlines.append({
                            'title': title,
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'published': article.get('publishedAt', '')[:10],
                            'url': article.get('url', '')
                        })
                print(f"[NEWS] Found {len(headlines)} news articles")
            else:
                print(f"[WARN] NewsAPI: {data.get('message', 'No data')}")

        except Exception as e:
            print(f"[ERROR] News fetch error: {e}")

        return headlines

    # ── FinBERT Sentiment Analysis ──────────────────────────────
    def analyze_sentiment_finbert(self, headlines):
        """Analyze sentiment using FinBERT (or keyword fallback)."""
        if not headlines:
            return 0, []

        finbert = get_finbert()
        results = []

        for item in headlines:
            title = item['title']
            try:
                if finbert:
                    # FinBERT inference (max 512 tokens)
                    output = finbert(title[:512])[0]
                    label = output['label']
                    score = output['score']

                    if label == 'positive':
                        sentiment = score
                    elif label == 'negative':
                        sentiment = -score
                    else:
                        sentiment = 0.0
                else:
                    # Keyword-based fallback
                    sentiment, label, score = self._fallback_sentiment(title)

                results.append({
                    'headline': title[:120],
                    'source': item.get('source', 'Unknown'),
                    'published': item.get('published', ''),
                    'label': label,
                    'confidence': round(float(score), 3),
                    'sentiment': round(float(sentiment), 3)
                })
            except Exception:
                results.append({
                    'headline': title[:120],
                    'source': item.get('source', 'Unknown'),
                    'published': item.get('published', ''),
                    'label': 'neutral',
                    'confidence': 0.5,
                    'sentiment': 0.0
                })

        avg_sentiment = float(np.mean([r['sentiment'] for r in results])) if results else 0
        return round(avg_sentiment, 3), results

    def _fallback_sentiment(self, text):
        """Keyword-based sentiment fallback when FinBERT is unavailable."""
        text_lower = text.lower()
        positive = ['surge', 'rise', 'gain', 'beat', 'growth', 'profit',
                     'soar', 'rally', 'bullish', 'upgrade', 'record', 'high']
        negative = ['fall', 'drop', 'loss', 'miss', 'decline', 'warn',
                     'crash', 'plunge', 'bearish', 'downgrade', 'cut', 'low']

        pos = sum(1 for w in positive if w in text_lower)
        neg = sum(1 for w in negative if w in text_lower)

        if pos > neg:
            return 0.6, 'positive', 0.6
        elif neg > pos:
            return -0.6, 'negative', 0.6
        return 0.0, 'neutral', 0.5

    # ── Technical Analysis ──────────────────────────────────────
    def analyze_technical(self, hist_data):
        """Technical analysis: MA crossover, RSI, MACD."""
        if hist_data is None or len(hist_data) < 5:
            return 0.5, {}, []

        df = hist_data.copy()

        # Moving Averages
        df['MA_5'] = df['Close'].rolling(5).mean()
        df['MA_20'] = df['Close'].rolling(20).mean()

        # RSI (14-period)
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss.replace(0, np.inf)
        df['RSI'] = 100 - (100 / (1 + rs))

        # MACD
        ema12 = df['Close'].ewm(span=12).mean()
        ema26 = df['Close'].ewm(span=26).mean()
        df['MACD'] = ema12 - ema26
        df['Signal_Line'] = df['MACD'].ewm(span=9).mean()

        latest = df.iloc[-1]
        scores = []
        details = {}

        # MA Crossover
        if pd.notna(latest.get('MA_5')) and pd.notna(latest.get('MA_20')):
            ma_signal = 1 if latest['MA_5'] > latest['MA_20'] else 0
            scores.append(ma_signal)
            details['ma_crossover'] = 'bullish' if ma_signal else 'bearish'

        # RSI
        if pd.notna(latest.get('RSI')):
            rsi = float(latest['RSI'])
            details['rsi'] = round(rsi, 1)
            if rsi < 30:
                scores.append(1)    # Oversold → buy
                details['rsi_signal'] = 'oversold'
            elif rsi > 70:
                scores.append(0)    # Overbought → sell
                details['rsi_signal'] = 'overbought'
            else:
                scores.append(0.5)
                details['rsi_signal'] = 'neutral'

        # MACD
        if pd.notna(latest.get('MACD')) and pd.notna(latest.get('Signal_Line')):
            macd_bull = 1 if latest['MACD'] > latest['Signal_Line'] else 0
            scores.append(macd_bull)
            details['macd'] = 'bullish' if macd_bull else 'bearish'

        # Price trend (5-day)
        if len(df) >= 5:
            pct = (df['Close'].iloc[-1] - df['Close'].iloc[-5]) / df['Close'].iloc[-5]
            details['five_day_change'] = round(float(pct * 100), 2)
            scores.append(1 if pct > 0 else 0)

        tech_score = float(np.mean(scores)) if scores else 0.5

        # Build chart data (last 30 trading days)
        chart_data = []
        for idx, row in df.tail(30).iterrows():
            point = {
                'date': idx.strftime('%Y-%m-%d'),
                'close': round(float(row['Close']), 2),
                'volume': int(row['Volume']) if pd.notna(row['Volume']) else 0,
            }
            if pd.notna(row.get('MA_5')):
                point['ma5'] = round(float(row['MA_5']), 2)
            if pd.notna(row.get('MA_20')):
                point['ma20'] = round(float(row['MA_20']), 2)
            chart_data.append(point)

        print(f"[TECH] Technical Score: {tech_score:.2f}")
        return round(tech_score, 3), details, chart_data

    # ── Hybrid Prediction ───────────────────────────────────────
    def predict_stock(self, ticker):
        """Main prediction: combines FinBERT sentiment + technicals."""
        print(f"\n{'='*50}")
        print(f"PREDICTING: {ticker}")
        print(f"{'='*50}")

        # 1 — Stock data
        hist, stock_info = self.get_stock_data(ticker)
        if hist is None:
            return {'error': f'Could not get data for {ticker}'}

        # 2 — News sentiment (FinBERT)
        headlines = self.get_news_headlines(ticker)
        sentiment, sentiment_details = self.analyze_sentiment_finbert(headlines)

        # 3 — Technical analysis
        tech_score, tech_details, chart_data = self.analyze_technical(hist)

        # 4 — Dynamic weighting
        news_count = len(sentiment_details)
        if news_count > 0:
            news_weight = 0.7
            tech_weight = 0.3
            news_prob = (sentiment + 1) / 2   # Map -1..+1 → 0..1
            final_prob = (news_prob * news_weight) + (tech_score * tech_weight)
            print(f"\n[WEIGHTS] NEWS={news_weight:.0%}, TECH={tech_weight:.0%}")
        else:
            news_weight = 0.0
            tech_weight = 1.0
            final_prob = tech_score
            print("\n[WARN] No news -> 100% technical analysis")

        # 5 — Signal decision
        current_price = round(float(hist['Close'].iloc[-1]), 2)
        prev_close = round(float(hist['Close'].iloc[-2]), 2) if len(hist) > 1 else current_price
        change = round(current_price - prev_close, 2)
        change_pct = round((change / prev_close) * 100, 2) if prev_close else 0

        if final_prob > 0.6:
            signal = "STRONG BUY"
        elif final_prob > 0.55:
            signal = "BUY"
        elif final_prob > 0.52:
            signal = "WEAK BUY"
        elif final_prob < 0.4:
            signal = "STRONG SELL"
        elif final_prob < 0.45:
            signal = "SELL"
        elif final_prob < 0.48:
            signal = "WEAK SELL"
        else:
            signal = "HOLD"

        signal_type = 'buy' if 'BUY' in signal else ('sell' if 'SELL' in signal else 'hold')

        print(f"\n[RESULT] {signal}")
        print(f"   Confidence: {final_prob:.1%}")
        print(f"   Price: ${current_price:.2f}")

        return {
            'ticker': ticker,
            'name': stock_info.get('name', ticker) if stock_info else ticker,
            'current_price': current_price,
            'prev_close': prev_close,
            'change': change,
            'change_pct': change_pct,
            'signal': signal,
            'signal_type': signal_type,
            'confidence': round(float(final_prob), 3),
            'weights': {
                'news': news_weight,
                'technical': tech_weight
            },
            'sentiment': {
                'score': sentiment,
                'news_count': news_count,
                'details': sentiment_details
            },
            'technical': tech_details,
            'chart_data': chart_data,
            'stock_info': stock_info if stock_info else {},
            'timestamp': datetime.now().isoformat()
        }


# ── Standalone Test ─────────────────────────────────────────────
def test_predictor():
    """Test function — called from main.py."""
    print("Testing Hybrid Stock Predictor (FinBERT)")
    print("=" * 50)

    from dotenv import load_dotenv
    import os
    load_dotenv()

    news_key = os.getenv("NEWS_API_KEY", "")
    finnhub_key = os.getenv("FINNHUB_KEY", "")

    if not news_key:
        print("[WARN] NEWS_API_KEY not set in .env")
        return

    predictor = HybridStockPredictor(news_key, finnhub_key)

    test_stocks = ["AAPL", "TSLA", "GOOGL"]
    results = []

    for stock in test_stocks:
        try:
            result = predictor.predict_stock(stock)
            results.append(result)
            print()
        except Exception as e:
            print(f"[ERROR] Error predicting {stock}: {e}")

    print(f"{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")

    for result in results:
        if isinstance(result, dict) and 'error' not in result:
            print(f"  {result['signal']} {result['ticker']} "
                  f"(${result['current_price']})")


if __name__ == "__main__":
    test_predictor()