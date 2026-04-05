# test_my_apis.py
"""
📡 API TESTER - Enter your keys and run!
Get free keys from:
1. NewsAPI: https://newsapi.org/register
2. Finnhub: https://finnhub.io/register
"""

import requests
import time
from datetime import datetime, timedelta

# =================================================================
# 🔐 ENTER YOUR API KEYS HERE (between the quotes):
# =================================================================

NEWS_API_KEY = "1112d012fead439ab1a6b13d8af7725a"        # From https://newsapi.org/register
FINNHUB_API_KEY = "d51fnd9r01qhn003ng90d51fnd9r01qhn003ng9g"     # From https://finnhub.io/register

# =================================================================
# DON'T EDIT BELOW THIS LINE
# =================================================================

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"🔍 {text}")
    print("=" * 60)

def test_newsapi():
    """Test NewsAPI.org"""
    print_header("Testing NewsAPI.org")
    
    if NEWS_API_KEY == "YOUR_NEWSAPI_KEY_HERE":
        print("❌ No API key provided!")
        print("👉 Get FREE key from: https://newsapi.org/register")
        print("👉 Then replace 'YOUR_NEWSAPI_KEY_HERE' with your actual key")
        return False
    
    try:
        print(f"📡 Using key: {NEWS_API_KEY[:8]}...{NEWS_API_KEY[-8:]}")
        
        # Test 1: Get news for Apple
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': 'Apple',
            'apiKey': NEWS_API_KEY,
            'pageSize': 3,
            'language': 'en',
            'sortBy': 'publishedAt'
        }
        
        print("\n📰 Fetching Apple news...")
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = data.get('articles', [])
            print(f"✅ SUCCESS! Found {len(articles)} articles")
            
            for i, article in enumerate(articles, 1):
                title = article.get('title', 'No title')
                source = article.get('source', {}).get('name', 'Unknown')
                published = article.get('publishedAt', '')[:10]
                print(f"\n   {i}. {title[:80]}...")
                print(f"      📍 Source: {source}")
                print(f"      📅 Date: {published}")
            
            # Check rate limits
            print(f"\n📊 API Status:")
            print(f"   Total Results: {data.get('totalResults', 0)}")
            print(f"   Daily Limit: 100 requests/day (free tier)")
            
            return True
            
        else:
            error_msg = data.get('message', 'Unknown error')
            print(f"❌ API Error: {error_msg}")
            
            if error_msg == "API key missing or invalid":
                print("👉 Your API key is incorrect or expired")
                print("👉 Get new key: https://newsapi.org/register")
            elif "rate limited" in error_msg.lower():
                print("👉 You've exceeded daily limit (100 requests)")
                print("👉 Wait 24 hours or upgrade plan")
            
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - check internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check internet")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_finnhub():
    """Test Finnhub.io"""
    print_header("Testing Finnhub.io")
    
    if FINNHUB_API_KEY == "YOUR_FINNHUB_KEY_HERE":
        print("❌ No API key provided!")
        print("👉 Get FREE key from: https://finnhub.io/register")
        print("👉 Then replace 'YOUR_FINNHUB_KEY_HERE' with your actual key")
        return False
    
    try:
        print(f"📡 Using key: {FINNHUB_API_KEY[:8]}...{FINNHUB_API_KEY[-8:]}")
        
        # Test 1: Get stock quote (AAPL)
        print("\n📈 Fetching Apple stock quote...")
        url = "https://finnhub.io/api/v1/quote"
        params = {
            'symbol': 'AAPL',
            'token': FINNHUB_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        quote = response.json()
        
        if 'c' in quote and quote['c'] > 0:  # Current price exists
            print(f"✅ SUCCESS! Live Market Data:")
            print(f"   Current: ${quote['c']:.2f}")
            print(f"   Change: ${quote['d']:.2f} ({quote['dp']:.2f}%)")
            print(f"   High: ${quote['h']:.2f}")
            print(f"   Low: ${quote['l']:.2f}")
            print(f"   Volume: {quote.get('v', 0):,}")
        else:
            print(f"⚠️ No price data or zero price")
            print(f"   Response: {quote}")
        
        # Test 2: Get company news
        print("\n📰 Fetching recent Apple news...")
        url = "https://finnhub.io/api/v1/company-news"
        
        # Get dates (last 7 days)
        to_date = datetime.now()
        from_date = to_date - timedelta(days=7)
        
        params = {
            'symbol': 'AAPL',
            'from': from_date.strftime('%Y-%m-%d'),
            'to': to_date.strftime('%Y-%m-%d'),
            'token': FINNHUB_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        news_items = response.json()
        
        if isinstance(news_items, list) and len(news_items) > 0:
            print(f"✅ SUCCESS! Found {len(news_items)} news items")
            
            # Show top 3
            for i, news in enumerate(news_items[:3], 1):
                headline = news.get('headline', 'No headline')
                source = news.get('source', 'Unknown')
                date = news.get('datetime', 0)
                
                if date:
                    date_str = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
                else:
                    date_str = 'Unknown date'
                
                print(f"\n   {i}. {headline[:80]}...")
                print(f"      📍 Source: {source}")
                print(f"      📅 Date: {date_str}")
        else:
            print(f"⚠️ No news found or empty response")
        
        # Test 3: Get company profile (optional)
        print("\n🏢 Fetching Apple company profile...")
        url = "https://finnhub.io/api/v1/stock/profile2"
        params = {
            'symbol': 'AAPL',
            'token': FINNHUB_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        profile = response.json()
        
        if 'name' in profile:
            print(f"✅ SUCCESS! Company Info:")
            print(f"   Name: {profile.get('name')}")
            print(f"   Industry: {profile.get('finnhubIndustry', 'N/A')}")
            print(f"   Market Cap: ${profile.get('marketCapitalization', 0):,}")
            print(f"   Country: {profile.get('country', 'N/A')}")
        else:
            print(f"⚠️ No profile data")
        
        # Rate limit info
        print("\n📊 API Limits (Free Tier):")
        print("   60 calls/minute")
        print("   Unlimited calls/day")
        
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Request timeout - check internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - check internet")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_both_together():
    """Test integrated scenario - stock + news"""
    print_header("Testing Combined Scenario")
    
    if not NEWS_API_KEY.startswith("YOUR_") and not FINNHUB_API_KEY.startswith("YOUR_"):
        print("Simulating stock prediction pipeline...")
        
        try:
            # Get stock price from Finnhub
            url = "https://finnhub.io/api/v1/quote"
            params = {'symbol': 'TSLA', 'token': FINNHUB_API_KEY}
            response = requests.get(url, params=params, timeout=5)
            quote = response.json()
            
            # Get news from NewsAPI
            url = "https://newsapi.org/v2/everything"
            params = {'q': 'Tesla', 'apiKey': NEWS_API_KEY, 'pageSize': 1}
            response = requests.get(url, params=params, timeout=5)
            news_data = response.json()
            
            print("✅ Both APIs working together!")
            print(f"\n📊 Tesla Stock: ${quote.get('c', 'N/A')}")
            
            if news_data.get('status') == 'ok' and news_data.get('articles'):
                article = news_data['articles'][0]
                print(f"📰 Latest News: {article.get('title', 'No title')[:60]}...")
            
            print("\n🎉 Ready for stock prediction app!")
            return True
            
        except Exception as e:
            print(f"⚠️ Combined test error: {e}")
            return False
    else:
        print("⚠️ Need both API keys to run combined test")
        return False

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("🔐 API KEY TESTER - Stock Prediction Project")
    print("=" * 60)
    
    print("\n📋 Before you start:")
    print("1. Get FREE NewsAPI key: https://newsapi.org/register")
    print("2. Get FREE Finnhub key: https://finnhub.io/register")
    print("3. Replace the API keys at the TOP of this file")
    print("4. Run: python test_my_apis.py")
    
    # Check if keys are still placeholder
    if NEWS_API_KEY == "YOUR_NEWSAPI_KEY_HERE":
        print("\n❌ You haven't entered your NewsAPI key!")
    
    if FINNHUB_API_KEY == "YOUR_FINNHUB_KEY_HERE":
        print("❌ You haven't entered your Finnhub key!")
    
    if NEWS_API_KEY == "YOUR_NEWSAPI_KEY_HERE" or FINNHUB_API_KEY == "YOUR_FINNHUB_KEY_HERE":
        print("\n📝 Edit this file and replace the placeholder keys!")
        print("   Look for lines 17-18 in the code")
        return
    
    print("\n" + "=" * 60)
    print("🚀 Starting API Tests...")
    print("=" * 60)
    
    results = []
    
    # Test NewsAPI
    print("\n🔵 Testing NewsAPI...")
    newsapi_result = test_newsapi()
    results.append(("NewsAPI.org", newsapi_result))
    
    # Wait a bit between API calls
    time.sleep(1)
    
    # Test Finnhub
    print("\n🟢 Testing Finnhub...")
    finnhub_result = test_finnhub()
    results.append(("Finnhub.io", finnhub_result))
    
    # Test combined if both worked
    if newsapi_result and finnhub_result:
        time.sleep(1)
        combined_result = test_both_together()
        results.append(("Combined Test", combined_result))
    
    # Print summary
    print_header("TEST RESULTS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for api_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {api_name}")
    
    print(f"\n📊 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 EXCELLENT! All APIs are working!")
        print("You're ready to build the stock predictor!")
    elif passed >= 1:
        print(f"\n⚠️ Partial success - {total-passed} API(s) need fixing")
        print("Check the error messages above")
    else:
        print("\n❌ All tests failed. Check:")
        print("1. Internet connection")
        print("2. API keys are correct")
        print("3. No typos in keys")
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. If tests pass → Start building your app!")
    print("2. If tests fail → Fix the errors above")
    print("=" * 60)

if __name__ == "__main__":
    main()